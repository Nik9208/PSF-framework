import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.stats import skew, kurtosis
from sklearn.feature_selection import mutual_info_regression

# ---------------------------------------------------------
# Data Generators
# ---------------------------------------------------------

def lorenz_deriv(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

def generate_lorenz(dt=0.01, noise_std=0.0, steps=10000, skip=1000, state0=[1.0, 1.0, 1.0]):
    t = np.arange(0, (steps + skip) * dt, dt)
    states = odeint(lorenz_deriv, state0, t)
    x = states[skip:, 0]
    if noise_std > 0:
        x += np.random.randn(steps) * noise_std
    return x

def generate_ar1(a=0.9, noise_std=1.0, steps=10000, x0=None):
    x = np.zeros(steps)
    x[0] = x0 if x0 is not None else (np.random.randn() * noise_std)
    for t in range(1, steps):
        x[t] = a * x[t-1] + np.random.randn() * noise_std
    return x

# ---------------------------------------------------------
# Estimators & Checks
# ---------------------------------------------------------

def estimate_mi_k(ts, k=1, n_neighbors=5):
    """Estimate Mutual Information between t and t+k."""
    if len(ts) <= k: return 0.0
    x = ts[:-k].reshape(-1, 1)
    y = ts[k:]
    mi = mutual_info_regression(x, y, n_neighbors=n_neighbors)
    return mi[0]

def distribution_check(ts):
    return {
        "mean": float(np.mean(ts)),
        "variance": float(np.var(ts)),
        "skewness": float(skew(ts)),
        "kurtosis": float(kurtosis(ts))
    }

def temporal_profile(ts, max_k=20):
    profile = []
    for k in range(1, max_k + 1):
        mi = estimate_mi_k(ts, k)
        profile.append(float(mi))
    return profile

def divergence_check(ts_base, ts_perturbed):
    """Returns the divergence |x(t) - x'(t)| over time."""
    return np.abs(ts_base - ts_perturbed)

# ---------------------------------------------------------
# ICCS Proxy
# ---------------------------------------------------------

def estimate_stability(ts, num_windows=5):
    window_size = len(ts) // num_windows
    mis = []
    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        chunk = ts[start:end]
        if len(chunk) > 1:
            mi = estimate_mi_k(chunk, k=1)
            mis.append(mi)
    return np.mean(mis), np.var(mis)

def estimate_iccs_proxy(mi_mean, stability_variance):
    return max(0.0, mi_mean - 2.0 * np.sqrt(stability_variance))

# ---------------------------------------------------------
# Run Sanity Checks
# ---------------------------------------------------------

def run_sanity():
    print("Starting pre-ICCS Sanity Checks (v0.3)...")
    steps = 10000
    
    # 1. Generate Base Systems from v0.2 intersection
    lorenz_ts = generate_lorenz(dt=0.05, noise_std=0.0, steps=steps)
    # Normalize for fair distribution comparison
    lorenz_ts = (lorenz_ts - np.mean(lorenz_ts)) / np.std(lorenz_ts)
    
    ar_ts = generate_ar1(a=0.99, noise_std=1.0, steps=steps)
    ar_ts = (ar_ts - np.mean(ar_ts)) / np.std(ar_ts)
    
    results = {"Lorenz": {}, "AR1": {}}
    
    # --- Check 1: Distributions ---
    print("1. Checking distributions...")
    results["Lorenz"]["dist"] = distribution_check(lorenz_ts)
    results["AR1"]["dist"] = distribution_check(ar_ts)
    
    # --- Check 2: Temporal Structure (MI Decay) ---
    print("2. Computing MI decay curves (k=1..20)...")
    results["Lorenz"]["mi_decay"] = temporal_profile(lorenz_ts, max_k=20)
    results["AR1"]["mi_decay"] = temporal_profile(ar_ts, max_k=20)
    
    # --- Check 3: Divergence (Lyapunov proxy) ---
    print("3. Checking perturbation divergence...")
    # Lorenz perturbation
    delta = 1e-5
    lorenz_base_raw = generate_lorenz(dt=0.05, noise_std=0.0, steps=1000, state0=[1.0, 1.0, 1.0])
    lorenz_pert_raw = generate_lorenz(dt=0.05, noise_std=0.0, steps=1000, state0=[1.0 + delta, 1.0, 1.0])
    results["Lorenz"]["divergence"] = divergence_check(lorenz_base_raw, lorenz_pert_raw).tolist()
    
    # AR1 perturbation
    ar_base_raw = generate_ar1(a=0.99, noise_std=0.0, steps=1000, x0=1.0) # Zero noise to isolate divergence logic, though AR is stochastic. 
    # Actually, for AR1 we must use the exact same noise sequence to isolate initial condition divergence.
    noise_seq = np.random.randn(1000) * 1.0
    def gen_ar_with_noise(a, start, noise_array):
        x = np.zeros(len(noise_array))
        x[0] = start
        for t in range(1, len(noise_array)):
            x[t] = a * x[t-1] + noise_array[t]
        return x
    
    ar_base_raw = gen_ar_with_noise(0.99, 1.0, noise_seq)
    ar_pert_raw = gen_ar_with_noise(0.99, 1.0 + delta, noise_seq)
    results["AR1"]["divergence"] = divergence_check(ar_base_raw, ar_pert_raw).tolist()
    
    # --- Check 4: ICCS Proxy ---
    print("4. Computing ICCS...")
    l_mean, l_var = estimate_stability(lorenz_ts)
    a_mean, a_var = estimate_stability(ar_ts)
    
    results["Lorenz"]["iccs"] = estimate_iccs_proxy(l_mean, l_var)
    results["AR1"]["iccs"] = estimate_iccs_proxy(a_mean, a_var)
    
    # Save JSON
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(results_dir, "equal_mi_sanity_v0.3.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nResults saved to {json_path}")
    
    # --- Plotting ---
    plt.figure(figsize=(15, 5))
    
    # Plot 1: MI Decay
    plt.subplot(1, 2, 1)
    k_vals = range(1, 21)
    plt.plot(k_vals, results["Lorenz"]["mi_decay"], marker='o', label='Lorenz')
    plt.plot(k_vals, results["AR1"]["mi_decay"], marker='x', label='AR(1)')
    plt.title("Temporal Structure: MI Decay Profile")
    plt.xlabel("Lag (k)")
    plt.ylabel("Mutual Information I(X_t; X_{t+k})")
    plt.grid(True)
    plt.legend()
    
    # Plot 2: Divergence
    plt.subplot(1, 2, 2)
    plt.plot(results["Lorenz"]["divergence"][:500], label='Lorenz (Chaos)')
    plt.plot(results["AR1"]["divergence"][:500], label='AR(1) (Stable)', alpha=0.8)
    plt.yscale('log')
    plt.title(f"Divergence from perturbation $\delta=10^{{-5}}$")
    plt.xlabel("Time steps")
    plt.ylabel("Absolute Difference (log scale)")
    plt.grid(True)
    plt.legend()
    
    plot_path = os.path.join(results_dir, "equal_mi_sanity_plot.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")
    
    print("\n=== Pre-ICCS Sanity Checks Summary ===")
    print(f"Distributions - Lorenz Skew: {results['Lorenz']['dist']['skewness']:.2f}, Kurtosis: {results['Lorenz']['dist']['kurtosis']:.2f}")
    print(f"Distributions - AR(1) Skew:  {results['AR1']['dist']['skewness']:.2f}, Kurtosis: {results['AR1']['dist']['kurtosis']:.2f}")
    print(f"ICCS Lorenz: {results['Lorenz']['iccs']:.4f}")
    print(f"ICCS AR(1):  {results['AR1']['iccs']:.4f}")

if __name__ == "__main__":
    run_sanity()
