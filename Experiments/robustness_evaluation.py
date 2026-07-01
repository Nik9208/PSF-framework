import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
import json
from scipy.integrate import odeint
from psf import ICCS

# ---------------------------------------------------------
# Generators
# ---------------------------------------------------------
def lorenz_system(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def generate_lorenz(steps=2000, dt=0.01, skip=1000, noise=0.0):
    t = np.arange(0, (steps + skip) * dt, dt)
    state0 = [1.0, 1.0, 1.0]
    traj = odeint(lorenz_system, state0, t)
    x = traj[skip:, 0]
    std = np.std(x)
    return x + np.random.randn(steps) * std * noise

def generate_causal_system(steps=2000, coupling=0.8, noise_level=0.0):
    Z = np.random.randn(steps)
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        X[t] = 0.5 * X[t-1] + np.random.randn()
        Y[t] = 0.5 * Y[t-1] + coupling * X[t-1] + np.random.randn()
    
    std_x, std_y, std_z = np.std(X), np.std(Y), np.std(Z)
    X += np.random.randn(steps) * std_x * noise_level
    Y += np.random.randn(steps) * std_y * noise_level
    Z += np.random.randn(steps) * std_z * noise_level
    return X, Y, Z

def generate_mimic_system(steps=2000, coupling=1.35, noise_level=0.0):
    noise = max(0.01, 1.5 - coupling)
    t = np.arange(steps)
    X = np.sin(0.1 * t) + np.random.randn(steps) * noise
    Y = np.sin(0.1 * t + np.pi/4) + np.random.randn(steps) * noise
    Z = np.random.randn(steps)
    
    std_x, std_y, std_z = np.std(X), np.std(Y), np.std(Z)
    X += np.random.randn(steps) * std_x * noise_level
    Y += np.random.randn(steps) * std_y * noise_level
    Z += np.random.randn(steps) * std_z * noise_level
    return X, Y, Z

# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------
def calculate_delta_s(prof1, prof2):
    """Euclidean distance of relative deviation between two structural vectors."""
    v1 = np.array([prof1['M'], prof1['D_local'], prof1['TE_forward'], prof1['TE_reverse'], prof1['CMI']])
    v2 = np.array([prof2['M'], prof2['D_local'], prof2['TE_forward'], prof2['TE_reverse'], prof2['CMI']])
    
    diff = np.abs(v1 - v2)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_diff = np.where(v1 > 0, diff / v1, diff)
        rel_diff = np.nan_to_num(rel_diff)
    return np.linalg.norm(rel_diff)

def run_evaluation():
    # To keep the script execution time reasonable for the demo, 
    # we'll scale back the highest N slightly or skip extremely large loops if needed.
    N_list = [500, 1000, 5000]
    Noise_list = [0.0, 0.01, 0.05, 0.10]
    k_list = [5, 10, 20]
    
    results = []
    
    print("Computing Baseline Profile (Lorenz, N=5000, Noise=0, k=10)...")
    base_lorenz = generate_lorenz(steps=5000, noise=0.0)
    iccs_base = ICCS(k_neighbors_mi=10, k_neighbors_id=10)
    base_prof = iccs_base.fit(base_lorenz)
    
    print("Running Stability Evaluation...")
    total_iters = len(N_list) * len(Noise_list) * len(k_list)
    current = 0
    
    for N in N_list:
        for noise in Noise_list:
            for k in k_list:
                current += 1
                print(f"  [{current}/{total_iters}] Testing N={N}, Noise={noise}, k={k}")
                
                iccs = ICCS(k_neighbors_mi=k, k_neighbors_id=k)
                
                # 1. Feature Stability Test
                X = generate_lorenz(steps=N, noise=noise)
                prof = iccs.fit(X)
                stability_score = calculate_delta_s(base_prof, prof)
                
                # 2. Boundary Preservation Test
                X_causal, Y_causal, Z_causal = generate_causal_system(steps=N, coupling=0.8, noise_level=noise)
                X_mimic, Y_mimic, Z_mimic = generate_mimic_system(steps=N, coupling=1.35, noise_level=noise)
                
                prof_c = iccs.fit(X_causal, Y_causal, Z_causal)
                prof_m = iccs.fit(X_mimic, Y_mimic, Z_mimic)
                
                boundary_separation_score = prof_c['TE_forward'] - prof_m['TE_forward']
                
                results.append({
                    "N": N,
                    "Noise": noise,
                    "k": k,
                    "Stability_Delta_S": float(stability_score),
                    "Boundary_Separation_TE": float(boundary_separation_score),
                    "Raw_Lorenz_Profile": prof.vector,
                    "Raw_Causal_TE": float(prof_c['TE_forward']),
                    "Raw_Mimic_TE": float(prof_m['TE_forward'])
                })

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Results'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "robustness_results.json")
    
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved robustness evaluation to {out_path}")

if __name__ == "__main__":
    run_evaluation()
