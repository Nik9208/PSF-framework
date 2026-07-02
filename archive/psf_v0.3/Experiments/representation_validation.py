import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_regression

# ---------------------------------------------------------
# Base System: 2D Discrete Nonlinear Oscillator
# ---------------------------------------------------------

def generate_base_system(steps=10000, skip=1000, noise_std=0.01):
    """
    x_{t+1} = sin(x_t - y_t)
    y_{t+1} = cos(x_t + y_t)
    """
    X = np.zeros((steps + skip, 2))
    X[0] = [0.1, 0.1] # Initial conditions
    
    for t in range(1, steps + skip):
        x_prev, y_prev = X[t-1]
        x_new = np.sin(x_prev - y_prev) + np.random.randn() * noise_std
        y_new = np.cos(x_prev + y_prev) + np.random.randn() * noise_std
        X[t] = [x_new, y_new]
        
    return X[skip:]

# ---------------------------------------------------------
# Adversarial Bijective Transforms
# ---------------------------------------------------------

def transform_original(X):
    return X.copy()

def transform_scaling(X):
    # A = [[2, 0], [0, 0.5]]
    A = np.array([[2.0, 0.0], [0.0, 0.5]])
    return X @ A.T

def transform_rotation(X, theta=np.pi/4):
    # R = [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return X @ R.T

def transform_nonlinear_bijection(X):
    # T(x, y) = (x + x^3, y + y^3)
    return X + X**3

def transform_permutation(X):
    # T(x, y) = (y, x)
    return X[:, [1, 0]]

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi_2d(X_t, X_next, n_neighbors=5):
    """
    Proxy for mutual information of 2D states.
    Calculates MI(X_t ; x_{next}) + MI(X_t ; y_{next})
    """
    if len(X_t) < 2: return 0.0
    mi_x = mutual_info_regression(X_t, X_next[:, 0], n_neighbors=n_neighbors)[0]
    mi_y = mutual_info_regression(X_t, X_next[:, 1], n_neighbors=n_neighbors)[0]
    return float(mi_x + mi_y)

def estimate_stability(X, num_windows=5):
    window_size = len(X) // num_windows
    mis = []
    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        chunk = X[start:end]
        if len(chunk) > 1:
            mi = estimate_mi_2d(chunk[:-1], chunk[1:])
            mis.append(mi)
    return np.mean(mis), np.var(mis)

def estimate_iccs_proxy(mi_mean, stability_variance):
    return max(0.0, mi_mean - 2.0 * np.sqrt(stability_variance))

# ---------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Generating base system...")
    steps = 5000
    base_X = generate_base_system(steps=steps)
    
    transforms = {
        "Original": transform_original,
        "Scaling": transform_scaling,
        "Rotation": transform_rotation,
        "Cubic_Bijection": transform_nonlinear_bijection,
        "Permutation": transform_permutation
    }
    
    results = []
    transformed_states = {}
    
    print("\nRunning Observer Transforms...")
    for name, t_func in transforms.items():
        print(f"  Evaluating: {name}")
        # Apply transformation
        X_obs = t_func(base_X)
        transformed_states[name] = X_obs
        
        # Estimate MI on full series
        mi_full = estimate_mi_2d(X_obs[:-1], X_obs[1:])
        
        # Estimate stability via chunking
        mi_mean, stability_var = estimate_stability(X_obs)
        
        # Calculate ICCS
        iccs = estimate_iccs_proxy(mi_full, stability_var)
        
        results.append({
            "Observer": name,
            "MI": float(mi_full),
            "Stability_Var": float(stability_var),
            "ICCS": float(iccs)
        })

    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "adversarial_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nResults saved to {json_path}")
    
    # Print Table
    print("\n| Observer | MI | Stability Var | ICCS |")
    print("|---|---|---|---|")
    for r in results:
        print(f"| {r['Observer']} | {r['MI']:.4f} | {r['Stability_Var']:.4f} | {r['ICCS']:.4f} |")
        
    # Plot Phase Portraits
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    
    for i, (name, X_obs) in enumerate(transformed_states.items()):
        ax = axes[i]
        ax.scatter(X_obs[:, 0], X_obs[:, 1], alpha=0.1, s=1)
        ax.set_title(name)
        ax.set_xlabel("Dimension 1")
        ax.set_ylabel("Dimension 2")
        ax.grid(True)
        
    plt.tight_layout()
    plot_path = os.path.join(results_dir, "phase_portraits.png")
    plt.savefig(plot_path)
    print(f"Phase portraits saved to {plot_path}")

if __name__ == "__main__":
    run_experiment()
