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

def generate_lorenz(dt=0.01, steps=10000, skip=1000):
    state0 = [1.0, 1.0, 1.0]
    t = np.arange(0, (steps + skip) * dt, dt)
    states = odeint(lorenz_deriv, state0, t)
    # We use x-coordinate as our 1D time series
    return states[skip:, 0]

def generate_ar1(a=0.9, std=1.0, steps=10000):
    x = np.zeros(steps)
    x[0] = np.random.randn() * std
    for t in range(1, steps):
        x[t] = a * x[t-1] + np.random.randn() * std
    return x

def generate_oscillator(freq=1.0, noise_std=0.5, steps=10000, dt=0.01):
    t = np.arange(steps) * dt
    signal = np.sin(2 * np.pi * freq * t)
    noise = np.random.randn(steps) * noise_std
    return signal + noise

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi(x, y, n_neighbors=5):
    """Estimate Mutual Information between 1D arrays x and y."""
    # mutual_info_regression expects 2D array for X
    mi = mutual_info_regression(x.reshape(-1, 1), y, n_neighbors=n_neighbors)
    return mi[0]

def estimate_stability(ts, num_windows=5):
    """Estimate structural stability by calculating MI variance across windows.
       High stability = Low variance."""
    window_size = len(ts) // num_windows
    mis = []
    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        chunk = ts[start:end]
        if len(chunk) > 1:
            mi = estimate_mi(chunk[:-1], chunk[1:])
            mis.append(mi)
    variance = np.var(mis)
    return np.mean(mis), variance

def estimate_iccs_proxy(mi_mean, stability_variance):
    """
    Proxy for Information Conditioned Carrier Score (ICCS).
    For boundary testing: penalizes instability.
    ICCS ~ MI - penalty * variance
    """
    return max(0.0, mi_mean - 2.0 * np.sqrt(stability_variance))

# ---------------------------------------------------------
# Experiment Logic
# ---------------------------------------------------------

def run_experiment():
    print("Starting Equal MI Different Dynamics experiment...")
    steps = 10000
    
    # 1. Base System: Lorenz
    lorenz_ts = generate_lorenz(steps=steps)
    
    # Normalize for fair comparison
    lorenz_ts = (lorenz_ts - np.mean(lorenz_ts)) / np.std(lorenz_ts)
    
    # 2. Target MI
    print("Estimating MI for Lorenz...")
    lorenz_mi = estimate_mi(lorenz_ts[:-1], lorenz_ts[1:])
    lorenz_mean, lorenz_var = estimate_stability(lorenz_ts)
    lorenz_iccs = estimate_iccs_proxy(lorenz_mi, lorenz_var)
    
    print(f"Lorenz Target MI: {lorenz_mi:.4f}")
    
    # 3. Fit AR(1) to match Target MI
    print("Fitting AR(1) coefficient to match MI...")
    best_a = 0.0
    min_diff = float('inf')
    matched_ar_ts = None
    
    # Sweep AR coefficient
    for a in np.linspace(0.1, 0.99, 20):
        ar_ts = generate_ar1(a=a, steps=steps)
        ar_ts = (ar_ts - np.mean(ar_ts)) / np.std(ar_ts)
        mi = estimate_mi(ar_ts[:-1], ar_ts[1:])
        diff = abs(mi - lorenz_mi)
        if diff < min_diff:
            min_diff = diff
            best_a = a
            matched_ar_ts = ar_ts
            
    print(f"Matched AR(1) at a={best_a:.3f} with MI diff {min_diff:.4f}")
    
    ar_mi = estimate_mi(matched_ar_ts[:-1], matched_ar_ts[1:])
    ar_mean, ar_var = estimate_stability(matched_ar_ts)
    ar_iccs = estimate_iccs_proxy(ar_mi, ar_var)
    
    # 4. Generate Noisy Oscillator
    print("Generating Noisy Oscillator...")
    osc_ts = generate_oscillator(steps=steps, noise_std=1.0)
    osc_ts = (osc_ts - np.mean(osc_ts)) / np.std(osc_ts)
    osc_mi = estimate_mi(osc_ts[:-1], osc_ts[1:])
    osc_mean, osc_var = estimate_stability(osc_ts)
    osc_iccs = estimate_iccs_proxy(osc_mi, osc_var)
    
    # 5. Compile Results
    results = [
        {
            "System": "Lorenz",
            "MI": float(lorenz_mi),
            "Stability_Var": float(lorenz_var),
            "ICCS_Proxy": float(lorenz_iccs),
            "Notes": "chaotic attractor"
        },
        {
            "System": "AR(1)",
            "MI": float(ar_mi),
            "Stability_Var": float(ar_var),
            "ICCS_Proxy": float(ar_iccs),
            "Notes": f"stochastic matched (a={best_a:.3f})"
        },
        {
            "System": "Oscillator",
            "MI": float(osc_mi),
            "Stability_Var": float(osc_var),
            "ICCS_Proxy": float(osc_iccs),
            "Notes": "noisy periodic"
        }
    ]
    
    # Ensure directory exists
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Save JSON
    json_path = os.path.join(results_dir, "equal_mi_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nResults saved to {json_path}")
    
    # Save Plot
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(lorenz_ts[:500])
    plt.title(f"Lorenz (MI: {lorenz_mi:.2f})")
    
    plt.subplot(1, 3, 2)
    plt.plot(matched_ar_ts[:500])
    plt.title(f"AR(1) a={best_a:.2f} (MI: {ar_mi:.2f})")
    
    plt.subplot(1, 3, 3)
    plt.plot(osc_ts[:500])
    plt.title(f"Oscillator (MI: {osc_mi:.2f})")
    
    plot_path = os.path.join(results_dir, "equal_mi_plot.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")
    
    # Print Table
    print("\n| System | MI | Stability Var | ICCS Proxy | Notes |")
    print("|---|---|---|---|---|")
    for r in results:
        print(f"| {r['System']} | {r['MI']:.4f} | {r['Stability_Var']:.4f} | {r['ICCS_Proxy']:.4f} | {r['Notes']} |")

if __name__ == "__main__":
    run_experiment()
