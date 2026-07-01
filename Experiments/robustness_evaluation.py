import sys
import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from psf import ICCS

def lorenz_system(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def generate_lorenz(rng, steps=2000, dt=0.01, skip=1000, noise=0.0):
    t = np.arange(0, (steps + skip) * dt, dt)
    state0 = [1.0, 1.0, 1.0]
    traj = odeint(lorenz_system, state0, t)
    x = traj[skip:, 0]
    std = np.std(x)
    return x + rng.standard_normal(steps) * std * noise

def generate_ar1(rng, steps=2000, a=0.9, noise=0.0):
    X = np.zeros(steps)
    X[0] = rng.standard_normal()
    for i in range(1, steps):
        X[i] = a * X[i-1] + rng.standard_normal()
    std = np.std(X)
    return X + rng.standard_normal(steps) * std * noise

def generate_causal_system(rng, steps=2000, coupling=0.8, noise_level=0.0):
    Z = rng.standard_normal(steps)
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        X[t] = 0.5 * X[t-1] + rng.standard_normal()
        Y[t] = 0.5 * Y[t-1] + coupling * X[t-1] + rng.standard_normal()
    
    std_x, std_y, std_z = np.std(X), np.std(Y), np.std(Z)
    X += rng.standard_normal(steps) * std_x * noise_level
    Y += rng.standard_normal(steps) * std_y * noise_level
    Z += rng.standard_normal(steps) * std_z * noise_level
    return X, Y, Z

def generate_mimic_system(rng, steps=2000, coupling=1.35, noise_level=0.0):
    noise = max(0.01, 1.5 - coupling)
    t = np.arange(steps)
    X = np.sin(0.1 * t) + rng.standard_normal(steps) * noise
    Y = np.sin(0.1 * t + np.pi/4) + rng.standard_normal(steps) * noise
    Z = rng.standard_normal(steps)
    
    std_x, std_y, std_z = np.std(X), np.std(Y), np.std(Z)
    X += rng.standard_normal(steps) * std_x * noise_level
    Y += rng.standard_normal(steps) * std_y * noise_level
    Z += rng.standard_normal(steps) * std_z * noise_level
    return X, Y, Z

def get_rel_diff(v, base_v):
    if base_v == 0:
        return 0.0
    return abs(v - base_v) / abs(base_v)

def run_evaluation():
    SEED = 42
    
    noise_sweep = [0.0, 0.01, 0.05, 0.10, 0.20]
    n_sweep = [250, 500, 1000, 5000, 10000]
    k_sweep = [5, 10, 20, 50]
    
    conditions = []
    # Exp 1 & 3: Noise Sweep
    for noise in noise_sweep:
        conditions.append({"N": 5000, "noise": noise, "k": 10, "exp": "Noise"})
    # Exp 2: Sample Size Sweep
    for n in n_sweep:
        if n != 5000:
            conditions.append({"N": n, "noise": 0.0, "k": 10, "exp": "SampleSize"})
    # Exp 4: Hyperparameter Sweep
    for k_val in k_sweep:
        if k_val != 10:
            conditions.append({"N": 5000, "noise": 0.0, "k": k_val, "exp": "Hyperparameter"})

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Results'))
    os.makedirs(out_dir, exist_ok=True)
    raw_path = os.path.join(out_dir, "robustness_raw.csv")
    
    results = []
    baselines = {}
    
    for cond in conditions:
        N = cond["N"]
        noise = cond["noise"]
        k = cond["k"]
        exp = cond["exp"]
        print(f"Running Exp: {exp:<14} | N: {N:<5} | Noise: {noise:<4} | k: {k}")
        
        # Instantiate ICCS with current k
        iccs = ICCS(max_k_memory=10, k_neighbors_mi=k, k_neighbors_id=k)
        
        # We seed inside the loop to ensure exactly the same sequence 
        # is generated for the same parameters, enhancing reproducibility.
        rng = np.random.default_rng(SEED)
        
        X_lorenz = generate_lorenz(rng, steps=N, noise=noise)
        prof_lorenz = iccs.fit(X_lorenz)
        
        X_ar = generate_ar1(rng, steps=N, noise=noise)
        prof_ar = iccs.fit(X_ar)
        
        X_c, Y_c, Z_c = generate_causal_system(rng, steps=N, noise_level=noise)
        prof_c = iccs.fit(X_c, Y_c, Z_c)
        
        X_m, Y_m, Z_m = generate_mimic_system(rng, steps=N, noise_level=noise)
        prof_m = iccs.fit(X_m, Y_m, Z_m)
        
        system_profs = {
            "Lorenz": prof_lorenz,
            "AR1": prof_ar,
            "Causal": prof_c,
            "Mimic": prof_m
        }
        
        if N == 5000 and noise == 0.0 and k == 10:
            baselines = system_profs.copy()
            
        for sys_name, prof in system_profs.items():
            
            delta_M = get_rel_diff(prof['M'], baselines.get(sys_name, prof)['M'])
            delta_D = get_rel_diff(prof['D_local'], baselines.get(sys_name, prof)['D_local'])
            delta_TE = get_rel_diff(prof['TE_forward'], baselines.get(sys_name, prof)['TE_forward'])
            delta_CMI = get_rel_diff(prof['CMI'], baselines.get(sys_name, prof)['CMI'])
            
            delta_S_rel = float(np.linalg.norm([delta_M, delta_D, delta_TE, delta_CMI]))
            
            if sys_name == "Causal":
                gap = prof['TE_forward'] - prof_m['TE_forward']
                rel_gap = gap / (prof['TE_forward'] + prof_m['TE_forward'] + 1e-6)
            elif sys_name == "Mimic":
                gap = prof_c['TE_forward'] - prof['TE_forward']
                rel_gap = gap / (prof_c['TE_forward'] + prof['TE_forward'] + 1e-6)
            else:
                gap = 0.0
                rel_gap = 0.0
                
            results.append({
                "exp": exp,
                "seed": SEED,
                "system": sys_name,
                "noise": noise,
                "N": N,
                "k": k,
                "M": prof['M'],
                "D_local": prof['D_local'],
                "TE_forward": prof['TE_forward'],
                "TE_reverse": prof['TE_reverse'],
                "CMI": prof['CMI'],
                "Delta_M": delta_M,
                "Delta_D": delta_D,
                "Delta_TE": delta_TE,
                "Delta_CMI": delta_CMI,
                "Delta_S_rel": delta_S_rel,
                "Gap": gap,
                "RelGap": rel_gap
            })
            
    # Save CSV
    keys = results[0].keys()
    with open(raw_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Data saved to {raw_path}")
    generate_plots(results, out_dir)

def generate_plots(results, out_dir):
    plots_dir = os.path.join(out_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Filter for Exp1 (Noise)
    exp1 = [r for r in results if r["exp"] == "Noise" and r["k"] == 10]
    noises = sorted(list(set(r["noise"] for r in exp1)))
    
    sys_list = ["Lorenz", "AR1", "Causal", "Mimic"]
    
    def plot_metric(metric, filename, ylabel):
        plt.figure(figsize=(8, 5))
        for sys_name in sys_list:
            y = [r[metric] for r in exp1 if r["system"] == sys_name]
            plt.plot(noises, y, marker='o', label=sys_name)
        plt.xlabel("Relative Gaussian Noise Level")
        plt.ylabel(ylabel)
        plt.title(f"Degradation of {metric} under Noise (N=5000)")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_dir, filename))
        plt.close()
        
    plot_metric("Delta_M", "delta_M.png", "Relative Shift ΔM")
    plot_metric("Delta_D", "delta_D_local.png", "Relative Shift ΔD_local")
    plot_metric("Delta_TE", "delta_TE.png", "Relative Shift ΔTE+")
    plot_metric("Delta_CMI", "delta_CMI.png", "Relative Shift ΔCMI")
    
    # Boundary Preservation Plot
    causal_te = [r["TE_forward"] for r in exp1 if r["system"] == "Causal"]
    mimic_te = [r["TE_forward"] for r in exp1 if r["system"] == "Mimic"]
    rel_gap = [r["RelGap"] for r in exp1 if r["system"] == "Causal"]
    
    x = np.arange(len(noises))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.bar(x - width/2, causal_te, width, label='Causal TE+', color='royalblue')
    ax1.bar(x + width/2, mimic_te, width, label='Mimic TE+', color='lightcoral')
    ax1.set_xlabel('Relative Noise Level')
    ax1.set_ylabel('Absolute TE+')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{n*100:.0f}%" for n in noises])
    
    ax2 = ax1.twinx()
    ax2.plot(x, rel_gap, color='green', marker='D', linewidth=2, label='Relative Gap')
    ax2.set_ylabel('Relative Separation Gap', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.axhline(0.1, color='red', linestyle='--', label='Failure Threshold (0.1)')
    
    fig.suptitle('Boundary Preservation: Causal vs Mimic under Noise')
    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(plots_dir, "boundary_separation.png"))
    plt.close()

if __name__ == "__main__":
    run_evaluation()
