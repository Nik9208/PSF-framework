import os
import json
import numpy as np
from sklearn.feature_selection import mutual_info_regression
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------
# System Generators
# ---------------------------------------------------------

def generate_system_A(steps=2000, coupling=0.5):
    # X -> Y
    Z = np.random.randn(steps) # Unrelated Z for structural symmetry in tests
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        X[t] = 0.5 * X[t-1] + np.random.randn()
        Y[t] = 0.5 * Y[t-1] + coupling * X[t-1] + np.random.randn()
    return X, Y, Z

def generate_system_B(steps=2000, coupling=0.5):
    # Z -> X, Z -> Y
    Z = np.zeros(steps)
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        Z[t] = 0.8 * Z[t-1] + np.random.randn()
        X[t] = 0.5 * X[t-1] + coupling * Z[t-1] + np.random.randn()
        Y[t] = 0.5 * Y[t-1] + coupling * Z[t-1] + np.random.randn()
    return X, Y, Z

def generate_system_C(steps=2000, coupling=0.5):
    # Y -> X
    Z = np.random.randn(steps) # Unrelated Z
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        Y[t] = 0.5 * Y[t-1] + np.random.randn()
        X[t] = 0.5 * X[t-1] + coupling * Y[t-1] + np.random.randn()
    return X, Y, Z

def generate_system_D(steps=2000, coupling=0.5):
    # Predictive mimic (Independent harmonic temporal structure)
    # coupling acts inversely on noise to match MI
    noise = max(0.01, 1.5 - coupling)
    t = np.arange(steps)
    X = np.sin(0.1 * t) + np.random.randn(steps) * noise
    Y = np.sin(0.1 * t + np.pi/4) + np.random.randn(steps) * noise
    Z = np.random.randn(steps)
    return X, Y, Z

# ---------------------------------------------------------
# Estimators (Residual-based Proxies)
# ---------------------------------------------------------

def estimate_mi(source, target):
    s = source.reshape(-1, 1)
    return float(mutual_info_regression(s, target)[0])

def compute_residual(target, predictor):
    model = LinearRegression()
    model.fit(predictor.reshape(-1, 1), target)
    return target - model.predict(predictor.reshape(-1, 1))

def compute_fingerprint(X, Y, Z):
    X_prev, X_curr = X[:-1], X[1:]
    Y_prev, Y_curr = Y[:-1], Y[1:]
    Z_prev = Z[:-1]
    
    # Base predictive info
    MI_X_Y = estimate_mi(X_prev, Y_curr)
    MI_Y_X = estimate_mi(Y_prev, X_curr)
    Max_MI = max(MI_X_Y, MI_Y_X)
    
    # TE Proxies
    res_Y_given_Y = compute_residual(Y_curr, Y_prev)
    TE_XY = estimate_mi(X_prev, res_Y_given_Y)
    
    res_X_given_X = compute_residual(X_curr, X_prev)
    TE_YX = estimate_mi(Y_prev, res_X_given_X)
    
    # CMI Proxy
    res_X_given_Z = compute_residual(X_curr, Z_prev)
    res_Y_given_Z = compute_residual(Y_curr, Z_prev)
    CMI = estimate_mi(res_X_given_Z, res_Y_given_Z)
    
    return {
        "Max_MI": Max_MI,
        "TE_XY": TE_XY,
        "TE_YX": TE_YX,
        "CMI": CMI
    }

# ---------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------

def run_experiment():
    steps = 3000
    print("Tuning Systems for Predictive Equivalence...")
    
    # Base System A (X -> Y)
    X_A, Y_A, Z_A = generate_system_A(steps, coupling=0.8)
    fp_A = compute_fingerprint(X_A, Y_A, Z_A)
    target_mi = fp_A["Max_MI"]
    print(f"System A Target Max MI: {target_mi:.4f}")
    
    # Tune System B (Z -> X, Z -> Y)
    best_c_B = 0.0
    min_diff = float('inf')
    best_X_B, best_Y_B, best_Z_B = None, None, None
    for c in np.linspace(0.1, 1.5, 30):
        X_B, Y_B, Z_B = generate_system_B(steps, coupling=c)
        fp_B = compute_fingerprint(X_B, Y_B, Z_B)
        diff = abs(fp_B["Max_MI"] - target_mi)
        if diff < min_diff:
            min_diff = diff
            best_c_B = c
            best_X_B, best_Y_B, best_Z_B = X_B, Y_B, Z_B
    print(f"Matched System B at coupling={best_c_B:.3f} with MI diff {min_diff:.4f}")
    
    # Tune System C (Y -> X)
    best_c_C = 0.0
    min_diff_C = float('inf')
    best_X_C, best_Y_C, best_Z_C = None, None, None
    for c in np.linspace(0.1, 1.5, 30):
        X_C, Y_C, Z_C = generate_system_C(steps, coupling=c)
        fp_C = compute_fingerprint(X_C, Y_C, Z_C)
        diff = abs(fp_C["Max_MI"] - target_mi)
        if diff < min_diff_C:
            min_diff_C = diff
            best_c_C = c
            best_X_C, best_Y_C, best_Z_C = X_C, Y_C, Z_C
    print(f"Matched System C at coupling={best_c_C:.3f} with MI diff {min_diff_C:.4f}")
    
    # Tune System D (Predictive mimic)
    best_c_D = 0.0
    min_diff_D = float('inf')
    best_X_D, best_Y_D, best_Z_D = None, None, None
    for c in np.linspace(0.1, 1.5, 30):
        X_D, Y_D, Z_D = generate_system_D(steps, coupling=c)
        fp_D = compute_fingerprint(X_D, Y_D, Z_D)
        diff = abs(fp_D["Max_MI"] - target_mi)
        if diff < min_diff_D:
            min_diff_D = diff
            best_c_D = c
            best_X_D, best_Y_D, best_Z_D = X_D, Y_D, Z_D
    print(f"Matched System D at pseudo-coupling={best_c_D:.3f} with MI diff {min_diff_D:.4f}")
    
    print("\nComputing Causal Fingerprints...")
    
    systems = {
        "System A (X->Y)": (X_A, Y_A, Z_A),
        "System B (Z->X,Y)": (best_X_B, best_Y_B, best_Z_B),
        "System C (Y->X)": (best_X_C, best_Y_C, best_Z_C),
        "System D (Mimic)": (best_X_D, best_Y_D, best_Z_D)
    }
    
    results = []
    for name, (X, Y, Z) in systems.items():
        fp = compute_fingerprint(X, Y, Z)
        results.append({
            "System": name,
            "Max_MI": fp["Max_MI"],
            "TE_XY": fp["TE_XY"],
            "TE_YX": fp["TE_YX"],
            "CMI": fp["CMI"]
        })
        
    # Output Table
    print("\n| System | Max Predictive MI | TE X->Y | TE Y->X | CMI (given Z) |")
    print("|---|---|---|---|---|")
    for r in results:
        print(f"| {r['System']} | {r['Max_MI']:.4f} | {r['TE_XY']:.4f} | {r['TE_YX']:.4f} | {r['CMI']:.4f} |")

    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, "causal_refinement_v0.1.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved JSON to {json_path}")

if __name__ == "__main__":
    run_experiment()
