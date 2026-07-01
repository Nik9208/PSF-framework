import os
import json
import numpy as np
from sklearn.feature_selection import mutual_info_regression

# ---------------------------------------------------------
# Base System
# ---------------------------------------------------------

def generate_base_system(steps=2000, skip=500, noise_std=0.01):
    X = np.zeros((steps + skip, 2))
    X[0] = [0.1, 0.1]
    
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

def transform_numerical_noise(X):
    return X + np.random.randn(*X.shape) * 1e-6

def transform_scaling(X):
    A = np.array([[2.0, 0.0], [0.0, 0.5]])
    return X @ A.T

def transform_rotation(X, theta=np.pi/4):
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return X @ R.T

def transform_cubic(X):
    return X + X**3

def transform_permutation(X):
    return X[:, [1, 0]]

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi_2d(X_t, X_next, n_neighbors=5):
    """ Proxy for mutual information of 2D states. """
    if len(X_t) < 2: return 0.0
    mi_x = mutual_info_regression(X_t, X_next[:, 0], n_neighbors=n_neighbors)[0]
    mi_y = mutual_info_regression(X_t, X_next[:, 1], n_neighbors=n_neighbors)[0]
    return float(mi_x + mi_y)

def compute_memory_profile(X, max_k=10):
    profile = []
    for k in range(1, max_k + 1):
        mi = estimate_mi_2d(X[:-k], X[k:])
        profile.append(mi)
    return profile

# ---------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Generating base system...")
    base_X = generate_base_system(steps=2000)
    
    transforms = {
        "Original": transform_original,
        "Numerical_Noise": transform_numerical_noise,
        "Scaling": transform_scaling,
        "Rotation": transform_rotation,
        "Cubic_Bijection": transform_cubic,
        "Permutation": transform_permutation
    }
    
    profiles = {}
    M_values = {}
    
    print("\nEvaluating Observers...")
    for name, t_func in transforms.items():
        print(f"  Evaluating: {name}")
        X_obs = t_func(base_X)
        prof = compute_memory_profile(X_obs, max_k=10)
        profiles[name] = prof
        M_values[name] = sum(prof)
        
    base_M = M_values["Original"]
    base_prof = np.array(profiles["Original"])
    
    results = []
    
    for name in transforms.keys():
        M = M_values[name]
        prof = np.array(profiles[name])
        
        delta_M = abs(M - base_M) / base_M if base_M > 0 else 0
        delta_P = np.mean(np.abs(prof - base_prof) / base_prof) if np.all(base_prof > 0) else 0
        
        results.append({
            "Observer": name,
            "M": float(M),
            "Delta_M": float(delta_M),
            "Delta_P": float(delta_P),
            "Profile": [float(p) for p in prof]
        })
        
    # Set epsilon threshold based on numerical noise identity test
    epsilon = [r["Delta_M"] for r in results if r["Observer"] == "Numerical_Noise"][0]
    # Add a small buffer to epsilon for practical tolerance
    epsilon = epsilon + 0.01 
    print(f"\nEmpirical Tolerance (epsilon): {epsilon:.4f}")

    # Output Table
    print("\n| Observer | M | Delta M | Profile distance | Status |")
    print("|---|---|---|---|---|")
    for r in results:
        status = "PASS" if r["Delta_M"] <= epsilon else "FAIL"
        print(f"| {r['Observer']} | {r['M']:.4f} | {r['Delta_M']:.4f} | {r['Delta_P']:.4f} | {status} |")
        
    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "representation_refinement_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")

if __name__ == "__main__":
    run_experiment()
