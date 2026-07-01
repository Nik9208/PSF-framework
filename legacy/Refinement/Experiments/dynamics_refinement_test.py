import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.spatial import distance_matrix
from sklearn.feature_selection import mutual_info_regression

# ---------------------------------------------------------
# System Generators
# ---------------------------------------------------------

def lorenz_system(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def generate_lorenz(steps=2000, dt=0.01, skip=1000):
    t = np.arange(0, (steps + skip) * dt, dt)
    state0 = [1.0, 1.0, 1.0]
    traj = odeint(lorenz_system, state0, t)
    return traj[skip:, 0] # Return X coordinate

def generate_ar1(a=0.9, noise_std=1.0, steps=2000):
    X = np.zeros(steps)
    X[0] = np.random.randn() * noise_std
    for i in range(1, steps):
        X[i] = a * X[i-1] + np.random.randn() * noise_std
    return X

def generate_oscillator(freq=0.1, noise_std=0.5, steps=2000):
    t = np.arange(steps)
    X = np.sin(2 * np.pi * freq * t) + np.random.randn(steps) * noise_std
    return X

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi(source, target, n_neighbors=5):
    if len(source) < 2: return 0.0
    s = source.reshape(-1, 1)
    mi = mutual_info_regression(s, target, n_neighbors=n_neighbors)
    return float(mi[0])

def compute_memory_profile(X, max_k=10):
    profile = []
    for k in range(1, max_k + 1):
        mi = estimate_mi(X[:-k], X[k:])
        profile.append(mi)
    return profile

def compute_rqa(X, epsilon_quantile=0.1, l_min=2, max_pts=1000):
    # Subsample for RQA if too long to save time
    if len(X) > max_pts:
        X = X[:max_pts]
    X_reshaped = X.reshape(-1, 1)
    D = distance_matrix(X_reshaped, X_reshaped)
    
    # Dynamic threshold based on data distribution
    epsilon = np.quantile(D[np.triu_indices_from(D, k=1)], epsilon_quantile)
    R = D < epsilon
    
    N = len(X)
    RR = np.sum(R) / (N * N)
    
    diag_pts_total = 0
    diag_pts_in_lines = 0
    for k in range(1, N):
        d = np.diag(R, k)
        diag_pts_total += np.sum(d)
        
        # Count lengths of consecutive 1s
        padded = np.pad(d, (1, 1), mode='constant')
        diffs = np.diff(padded.astype(int))
        starts = np.where(diffs == 1)[0]
        ends = np.where(diffs == -1)[0]
        lengths = ends - starts
        valid_lengths = lengths[lengths >= l_min]
        diag_pts_in_lines += np.sum(valid_lengths)
        
    DET = diag_pts_in_lines / diag_pts_total if diag_pts_total > 0 else 0.0
    return float(RR), float(DET)

# ---------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Generating Systems and Tuning MI(k=1)...")
    steps = 2000
    
    # 1. Base Lorenz (Subsampled to lower excessive short-term MI)
    X_lorenz_raw = generate_lorenz(steps=steps*10)
    X_lorenz = X_lorenz_raw[::10]
    target_mi = estimate_mi(X_lorenz[:-1], X_lorenz[1:])
    print(f"Lorenz P(1) Target: {target_mi:.4f}")
    
    # 2. Match AR(1)
    best_a = 0.0
    min_diff = float('inf')
    best_X_ar = None
    for a in np.linspace(0.8, 0.99, 20):
        X_ar = generate_ar1(a=a, steps=steps)
        mi = estimate_mi(X_ar[:-1], X_ar[1:])
        diff = abs(mi - target_mi)
        if diff < min_diff:
            min_diff = diff
            best_a = a
            best_X_ar = X_ar
    print(f"Matched AR(1) at a={best_a:.3f} with P(1) diff {min_diff:.4f}")
    
    # 3. Match Oscillator
    best_noise = 0.0
    min_diff_osc = float('inf')
    best_X_osc = None
    for noise in np.linspace(0.1, 2.0, 20):
        X_osc = generate_oscillator(noise_std=noise, steps=steps)
        mi = estimate_mi(X_osc[:-1], X_osc[1:])
        diff = abs(mi - target_mi)
        if diff < min_diff_osc:
            min_diff_osc = diff
            best_noise = noise
            best_X_osc = X_osc
    print(f"Matched Oscillator at noise={best_noise:.3f} with P(1) diff {min_diff_osc:.4f}")
    
    # 4. Compute Fingerprints
    print("\nComputing Dynamics Fingerprints...")
    systems = {
        "Lorenz (Chaos)": X_lorenz,
        "AR(1) (Stochastic)": best_X_ar,
        "Oscillator (Periodic)": best_X_osc
    }
    
    results = []
    profiles = {}
    
    for name, X in systems.items():
        print(f"  Analyzing {name}...")
        profile = compute_memory_profile(X, max_k=10)
        profiles[name] = profile
        area = sum(profile)
        rr, det = compute_rqa(X)
        
        results.append({
            "System": name,
            "P(1)": float(profile[0]),
            "Memory_Area": float(area),
            "RR": float(rr),
            "DET": float(det),
            "P_Profile": [float(p) for p in profile]
        })

    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "dynamics_refinement_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")
    
    # Output Table
    print("\n| System | P(1) | Memory Area | RR | DET |")
    print("|---|---|---|---|---|")
    for r in results:
        print(f"| {r['System']} | {r['P(1)']:.4f} | {r['Memory_Area']:.4f} | {r['RR']:.4f} | {r['DET']:.4f} |")
        
    # Plot P(k)
    plt.figure(figsize=(10, 6))
    for name, prof in profiles.items():
        plt.plot(range(1, 11), prof, marker='o', label=name)
    plt.xlabel("Lag (k)")
    plt.ylabel("Predictive Information P(k)")
    plt.title("Memory Profile")
    plt.legend()
    plt.grid(True)
    
    plot_path = os.path.join(results_dir, "memory_profile.png")
    plt.savefig(plot_path)
    print(f"Saved plot to {plot_path}")

if __name__ == "__main__":
    run_experiment()
