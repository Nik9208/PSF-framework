import os
import json
import numpy as np
from scipy.stats import rankdata
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

def rank_transform(X):
    """ X -> rank(X) / (N - 1) """
    ranks = np.zeros_like(X)
    for dim in range(X.shape[1]):
        ranks[:, dim] = rankdata(X[:, dim]) / (len(X) - 1)
    return ranks

# ---------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Generating base system...")
    base_X = generate_base_system(steps=2000)
    
    transforms = {
        "Original": transform_original,
        "Scaling": transform_scaling,
        "Rotation": transform_rotation,
        "Cubic_Bijection": transform_cubic,
        "Permutation": transform_permutation
    }
    
    results = []
    
    # 1. Calculate Baselines
    print("Evaluating Original System Baseline...")
    X_base = transforms["Original"](base_X)
    X_base_rank = rank_transform(X_base)
    
    prof_base_raw = compute_memory_profile(X_base, max_k=10)
    prof_base_rank = compute_memory_profile(X_base_rank, max_k=10)
    
    M_base_raw = sum(prof_base_raw)
    M_base_rank = sum(prof_base_rank)
    
    # 2. Evaluate Observers
    print("\nEvaluating Representations...")
    for name, t_func in transforms.items():
        print(f"  Evaluating: {name}")
        X_obs = t_func(base_X)
        X_obs_rank = rank_transform(X_obs)
        
        prof_raw = compute_memory_profile(X_obs, max_k=10)
        prof_rank = compute_memory_profile(X_obs_rank, max_k=10)
        
        M_raw = sum(prof_raw)
        M_rank = sum(prof_rank)
        
        delta_M_raw = abs(M_raw - M_base_raw) / M_base_raw if M_base_raw > 0 else 0
        delta_M_rank = abs(M_rank - M_base_rank) / M_base_rank if M_base_rank > 0 else 0
        
        results.append({
            "Observer": name,
            "M_raw": float(M_raw),
            "Delta_M_raw": float(delta_M_raw),
            "M_rank": float(M_rank),
            "Delta_M_rank": float(delta_M_rank)
        })

    # Output Table
    print("\n| Observer | M_raw | Delta_M_raw | M_rank | Delta_M_rank |")
    print("|---|---|---|---|---|")
    for r in results:
        print(f"| {r['Observer']} | {r['M_raw']:.4f} | {r['Delta_M_raw']:.4f} | {r['M_rank']:.4f} | {r['Delta_M_rank']:.4f} |")
        
    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "rank_mi_refinement_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")

if __name__ == "__main__":
    run_experiment()
