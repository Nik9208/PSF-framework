import os
import json
import numpy as np
from sklearn.neighbors import NearestNeighbors

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
# Estimator (Levina-Bickel MLE Intrinsic Dimension)
# ---------------------------------------------------------

def compute_local_dimension(X, k=10):
    """
    Maximum Likelihood Estimator of Intrinsic Dimensionality (Levina & Bickel, 2004)
    """
    if len(X) <= k:
        return 0.0
    
    # We query k+1 neighbors because the first neighbor is the point itself (distance 0)
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='auto').fit(X)
    distances, _ = nbrs.kneighbors(X)
    
    # Exclude the point itself
    distances = distances[:, 1:]
    
    # To avoid log(0) or div by 0, add small epsilon to distances
    distances = distances + 1e-10
    
    # R_k is the distance to the k-th neighbor
    R_k = distances[:, -1]
    
    # Compute the term for each point
    # d(x_i) = [ 1/(k-1) * sum_{j=1}^{k-1} log(R_k / R_j) ]^{-1}
    log_ratios = np.log(R_k[:, np.newaxis] / distances[:, :-1])
    
    # Mean over the k-1 neighbors
    mean_log_ratios = np.mean(log_ratios, axis=1)
    
    # Avoid division by zero if all neighbors are at exactly the same distance
    valid = mean_log_ratios > 0
    
    local_dims = np.zeros(len(X))
    local_dims[valid] = 1.0 / mean_log_ratios[valid]
    
    # Return the global average of local dimensions
    return float(np.mean(local_dims))

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
    
    results = []
    
    # 1. Calculate Baseline
    print("Evaluating Original System Baseline...")
    X_base = transforms["Original"](base_X)
    D_base = compute_local_dimension(X_base, k=15)
    
    # 2. Evaluate Observers
    print("\nEvaluating Representations for Local Dimension (D_local)...")
    for name, t_func in transforms.items():
        print(f"  Evaluating: {name}")
        X_obs = t_func(base_X)
        
        D_obs = compute_local_dimension(X_obs, k=15)
        
        delta_D = abs(D_obs - D_base) / D_base if D_base > 0 else 0
        
        results.append({
            "Observer": name,
            "D_local": float(D_obs),
            "Delta_D": float(delta_D)
        })

    # Set epsilon threshold to 5% as per protocol
    epsilon = 0.05
    print(f"\nEmpirical Tolerance (epsilon): {epsilon:.4f}")

    # Output Table
    print("\n| Observer | D_local | Delta D | Status |")
    print("|---|---|---|---|")
    for r in results:
        status = "PASS" if r["Delta_D"] <= epsilon else "FAIL"
        print(f"| {r['Observer']} | {r['D_local']:.4f} | {r['Delta_D']:.4f} | {status} |")
        
    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "local_dimension_refinement_v0.2.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")

if __name__ == "__main__":
    run_experiment()
