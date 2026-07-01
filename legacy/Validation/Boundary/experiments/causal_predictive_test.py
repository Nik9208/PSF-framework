import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_regression
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------
# Generators
# ---------------------------------------------------------

def generate_system_A(a=0.9, b=0.8, noise_std=1.0, steps=10000):
    """ Direct Causal: X_t -> Y_{t+1} """
    X = np.zeros(steps)
    Y = np.zeros(steps)
    X[0] = np.random.randn() * noise_std
    Y[0] = np.random.randn() * noise_std
    for t in range(1, steps):
        X[t] = a * X[t-1] + np.random.randn() * noise_std
        Y[t] = b * X[t-1] + np.random.randn() * noise_std
    return X, Y

def generate_system_B(a=0.9, b=0.8, noise_std=1.0, steps=10000):
    """ Common Driver: Z -> X, Z -> Y """
    Z = np.zeros(steps)
    X = np.zeros(steps)
    Y = np.zeros(steps)
    Z[0] = np.random.randn() * noise_std
    X[0] = np.random.randn() * noise_std
    Y[0] = np.random.randn() * noise_std
    for t in range(1, steps):
        Z[t] = a * Z[t-1] + np.random.randn() * noise_std
        X[t] = b * Z[t-1] + np.random.randn() * noise_std
        Y[t] = b * Z[t-1] + np.random.randn() * noise_std
    return X, Y, Z

def generate_system_C(a=0.9, b=0.8, noise_std=1.0, steps=10000):
    """ Reverse Predictive: Y_t -> X_{t+1} """
    X = np.zeros(steps)
    Y = np.zeros(steps)
    X[0] = np.random.randn() * noise_std
    Y[0] = np.random.randn() * noise_std
    for t in range(1, steps):
        Y[t] = a * Y[t-1] + np.random.randn() * noise_std
        X[t] = b * Y[t-1] + np.random.randn() * noise_std
    return X, Y

# ---------------------------------------------------------
# Estimators
# ---------------------------------------------------------

def estimate_mi(source, target, n_neighbors=5):
    if len(source) < 2: return 0.0
    s = source.reshape(-1, 1)
    mi = mutual_info_regression(s, target, n_neighbors=n_neighbors)
    return float(mi[0])

def estimate_stability(X, Y, num_windows=5):
    """ Estimates stability of MI(X_t ; Y_{t+1}) """
    window_size = len(X) // num_windows
    mis = []
    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        chunk_X = X[start:end]
        chunk_Y = Y[start:end]
        if len(chunk_X) > 1:
            mi = estimate_mi(chunk_X[:-1], chunk_Y[1:])
            mis.append(mi)
    return np.mean(mis), np.var(mis)

def estimate_iccs_proxy(mi_mean, stability_variance):
    return max(0.0, mi_mean - 2.0 * np.sqrt(stability_variance))

def estimate_cmi_proxy(X_t, Y_next, Z_t):
    """ Proxy for I(Y_{t+1}; X_t | Z_t) using residuals. """
    Z_reshaped = Z_t.reshape(-1, 1)
    
    # Regress X_t on Z_t
    model_x = LinearRegression().fit(Z_reshaped, X_t)
    res_x = X_t - model_x.predict(Z_reshaped)
    
    # Regress Y_next on Z_t
    model_y = LinearRegression().fit(Z_reshaped, Y_next)
    res_y = Y_next - model_y.predict(Z_reshaped)
    
    return estimate_mi(res_x, res_y)

# ---------------------------------------------------------
# Search & Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Starting Boundary Test #3: Causal vs Predictive Divergence")
    steps = 10000
    a_param = 0.9
    
    # 1. System A Baseline
    X_A, Y_A = generate_system_A(a=a_param, b=0.8, steps=steps)
    target_mi = estimate_mi(X_A[:-1], Y_A[1:])
    print(f"Target MI forward (System A): {target_mi:.4f}")
    
    # 2. Match System B
    print("Matching System B (Common Driver)...")
    best_b_B = 0.0
    min_diff = float('inf')
    best_XB, best_YB, best_ZB = None, None, None
    
    for b in np.linspace(0.1, 1.5, 30):
        X_B, Y_B, Z_B = generate_system_B(a=a_param, b=b, steps=steps)
        mi = estimate_mi(X_B[:-1], Y_B[1:])
        diff = abs(mi - target_mi)
        if diff < min_diff:
            min_diff = diff
            best_b_B = b
            best_XB, best_YB, best_ZB = X_B, Y_B, Z_B
            
    print(f"  Matched System B at b={best_b_B:.2f} with diff {min_diff:.4f}")
    
    # 3. Match System C
    print("Matching System C (Reverse)...")
    best_b_C = 0.0
    min_diff_C = float('inf')
    best_XC, best_YC = None, None
    
    for b in np.linspace(0.1, 1.5, 30):
        X_C, Y_C = generate_system_C(a=a_param, b=b, steps=steps)
        # Still measuring MI(X_t ; Y_{t+1}) as the forward target!
        mi = estimate_mi(X_C[:-1], Y_C[1:])
        diff = abs(mi - target_mi)
        if diff < min_diff_C:
            min_diff_C = diff
            best_b_C = b
            best_XC, best_YC = X_C, Y_C
            
    print(f"  Matched System C at b={best_b_C:.2f} with diff {min_diff_C:.4f}")
    
    # 4. Evaluate Metrics
    results = []
    
    # Function to package evaluations
    def evaluate(sys_name, X, Y, Z=None):
        mi_fwd = estimate_mi(X[:-1], Y[1:])
        mi_rev = estimate_mi(Y[:-1], X[1:])
        mi_mean, var = estimate_stability(X, Y)
        iccs = estimate_iccs_proxy(mi_mean, var)
        
        cmi = 0.0
        if Z is not None:
            cmi = estimate_cmi_proxy(X[:-1], Y[1:], Z[:-1])
        else:
            cmi = float('nan') # Undefined confounding
            
        return {
            "System": sys_name,
            "MI_forward": float(mi_fwd),
            "MI_reverse": float(mi_rev),
            "CMI_proxy": float(cmi),
            "ICCS": float(iccs)
        }
        
    results.append(evaluate("Direct causal (A)", X_A, Y_A))
    results.append(evaluate("Common driver (B)", best_XB, best_YB, Z=best_ZB))
    results.append(evaluate("Reverse (C)", best_XC, best_YC))
    
    # 5. Output Results
    print("\n| System | MI forward | MI reverse | CMI proxy | ICCS |")
    print("|---|---|---|---|---|")
    for r in results:
        cmi_str = f"{r['CMI_proxy']:.4f}" if not np.isnan(r['CMI_proxy']) else "N/A"
        print(f"| {r['System']} | {r['MI_forward']:.4f} | {r['MI_reverse']:.4f} | {cmi_str} | {r['ICCS']:.4f} |")
        
    # Save
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "causal_predictive_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")

if __name__ == "__main__":
    run_experiment()
