import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from sklearn.feature_selection import mutual_info_regression

# ---------------------------------------------------------
# Data Generators
# ---------------------------------------------------------

def lorenz_deriv(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

def generate_lorenz(dt=0.01, noise_std=0.0, steps=10000, skip=1000):
    state0 = [1.0, 1.0, 1.0]
    t = np.arange(0, (steps + skip) * dt, dt)
    states = odeint(lorenz_deriv, state0, t)
    x = states[skip:, 0]
    if noise_std > 0:
        x += np.random.randn(steps) * noise_std
    return (x - np.mean(x)) / np.std(x)

def generate_ar1(a=0.9, noise_std=1.0, steps=10000):
    x = np.zeros(steps)
    x[0] = np.random.randn() * noise_std
    for t in range(1, steps):
        x[t] = a * x[t-1] + np.random.randn() * noise_std
    return (x - np.mean(x)) / np.std(x)

def generate_nonlinear_memory(a=1.5, noise_std=0.5, steps=10000):
    """ Nonlinear stochastic memory: x_{t+1} = tanh(a * x_t) + eps """
    x = np.zeros(steps)
    x[0] = np.random.randn() * noise_std
    for t in range(1, steps):
        x[t] = np.tanh(a * x[t-1]) + np.random.randn() * noise_std
    return (x - np.mean(x)) / np.std(x)

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi(ts, n_neighbors=5):
    """Estimate Mutual Information between t and t+1."""
    if len(ts) < 2: return 0.0
    x = ts[:-1].reshape(-1, 1)
    y = ts[1:]
    mi = mutual_info_regression(x, y, n_neighbors=n_neighbors)
    return mi[0]

# ---------------------------------------------------------
# Grid Search Logic
# ---------------------------------------------------------

def run_search():
    print("Starting parameter search for Equal MI Intersection (v0.2)...")
    steps = 10000
    
    # 1. Sweep Lorenz Parameters (dt, noise_std)
    lorenz_configs = [
        {"dt": 0.01, "noise_std": 0.0},
        {"dt": 0.01, "noise_std": 0.5},
        {"dt": 0.05, "noise_std": 0.0},
        {"dt": 0.05, "noise_std": 0.5},
    ]
    
    print("Estimating MI for Lorenz candidates...")
    lorenz_results = []
    for cfg in lorenz_configs:
        ts = generate_lorenz(dt=cfg["dt"], noise_std=cfg["noise_std"], steps=steps)
        mi = estimate_mi(ts)
        lorenz_results.append({"config": cfg, "mi": float(mi), "ts": ts})
        print(f"  Lorenz dt={cfg['dt']}, noise={cfg['noise_std']} -> MI: {mi:.4f}")

    # 2. Sweep Stochastic Parameters (AR1 and Nonlinear)
    print("\nEstimating MI for Stochastic candidates...")
    stoch_results = []
    
    # AR(1) sweep
    for a in [0.5, 0.8, 0.9, 0.95, 0.99]:
        for noise in [0.5, 1.0, 2.0]:
            ts = generate_ar1(a=a, noise_std=noise, steps=steps)
            mi = estimate_mi(ts)
            stoch_results.append({"type": "AR(1)", "config": {"a": a, "noise": noise}, "mi": float(mi), "ts": ts})
            
    # Nonlinear Memory sweep
    for a in [0.5, 1.0, 2.0, 5.0, 10.0]:
        for noise in [0.1, 0.5, 1.0]:
            ts = generate_nonlinear_memory(a=a, noise_std=noise, steps=steps)
            mi = estimate_mi(ts)
            stoch_results.append({"type": "NonlinearMemory", "config": {"a": a, "noise": noise}, "mi": float(mi), "ts": ts})

    print(f"  Generated {len(stoch_results)} stochastic configurations.")

    # 3. Find Best Intersection
    print("\nFinding closest MI matches...")
    matches = []
    for lr in lorenz_results:
        for sr in stoch_results:
            diff = abs(lr["mi"] - sr["mi"])
            matches.append({
                "diff": diff,
                "lorenz": {"config": lr["config"], "mi": lr["mi"]},
                "stoch": {"type": sr["type"], "config": sr["config"], "mi": sr["mi"]},
                "l_ts": lr["ts"],
                "s_ts": sr["ts"]
            })
            
    # Sort by closest match
    matches.sort(key=lambda x: x["diff"])
    best_match = matches[0]
    
    print("\n=== Best Intersection ===")
    print(f"MI Difference: {best_match['diff']:.4f}")
    print(f"Lorenz: {best_match['lorenz']}")
    print(f"Stochastic: {best_match['stoch']}")
    
    # 4. Save best match for ICCS analysis
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    output_json = {
        "diff": best_match["diff"],
        "lorenz_target": best_match["lorenz"],
        "stochastic_match": best_match["stoch"]
    }
    
    json_path = os.path.join(results_dir, "equal_mi_search_v0.2.json")
    with open(json_path, "w") as f:
        json.dump(output_json, f, indent=4)
        
    print(f"\nSaved best match config to {json_path}")
    
    # Plot the pair
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(best_match["l_ts"][:500])
    plt.title(f"Lorenz (MI={best_match['lorenz']['mi']:.4f})")
    
    plt.subplot(1, 2, 2)
    plt.plot(best_match["s_ts"][:500])
    plt.title(f"{best_match['stoch']['type']} (MI={best_match['stoch']['mi']:.4f})")
    
    plot_path = os.path.join(results_dir, "equal_mi_search_plot.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"Saved plot to {plot_path}")

if __name__ == "__main__":
    run_search()
