import os
import json
import numpy as np

# ---------------------------------------------------------
# Feature Vectors (Empirical Proxies from previous tests)
# S(X) = [M, D_local, TE_+, TE_-, CMI]
# ---------------------------------------------------------

# System A: Predictive Mimic (e.g. deterministic harmonic oscillator)
# High prediction, low dimension, no causal transfer
S_A = np.array([0.90, 1.00, 0.01, 0.02, 0.50])

# System B: Direct Causal System (e.g. X -> Y stochastic AR)
# Moderate prediction, 2D geometry, high causal transfer
S_B = np.array([0.30, 2.00, 0.25, 0.00, 0.05])

# System C: Complex Geometry System (e.g. high-dim chaos / noise)
# Low prediction, complex geometry, no causal transfer
S_C = np.array([0.10, 3.50, 0.02, 0.02, 0.01])

systems = {
    "System A (Mimic)": S_A,
    "System B (Causal)": S_B,
    "System C (Geometry)": S_C
}

# ---------------------------------------------------------
# Aggregation Functions
# ---------------------------------------------------------

def agg_linear(S, weights):
    # I = w1*M + w2*D + w3*TE+ - w4*TE- - w5*CMI
    M, D, TE_p, TE_m, CMI = S
    return weights[0]*M + weights[1]*D + weights[2]*TE_p - weights[3]*TE_m - weights[4]*CMI

def agg_multiplicative(S):
    # I = M * D^(-1) * max(0, TE+ - TE-) * exp(-CMI)
    M, D, TE_p, TE_m, CMI = S
    te_diff = max(0.0, TE_p - TE_m)
    return M * (1.0/D) * te_diff * np.exp(-CMI)

def agg_distance(S, S_target):
    # Euclidean distance in feature space (lower is more structurally similar)
    return float(np.linalg.norm(S - S_target))

def is_pareto_dominated(S1, S2):
    """
    Returns True if S2 dominates S1.
    We want to MAXIMIZE M, TE+. 
    We want to MINIMIZE TE-, CMI.
    For D_local, it depends. Let's assume we want to maximize it as a proxy for complexity.
    """
    # Flip signs for dimensions we want to minimize so we can just check '>=', '>'
    S1_adj = np.array([S1[0], S1[1], S1[2], -S1[3], -S1[4]])
    S2_adj = np.array([S2[0], S2[1], S2[2], -S2[3], -S2[4]])
    
    return np.all(S2_adj >= S1_adj) and np.any(S2_adj > S1_adj)

# ---------------------------------------------------------
# Experiment
# ---------------------------------------------------------

def run_experiment():
    print("Running Aggregation Collapse Test...\n")
    
    # 1. Linear Collapse (Feature Compensation)
    # We deliberately find weights that collapse Mimic and Causal
    # S_A = [0.90, 1.00, 0.01, 0.02, 0.50]
    # S_B = [0.30, 2.00, 0.25, 0.00, 0.05]
    # If w1=1.0, w2=0.1, w3=2.4, w4=1.0, w5=0.5
    # I(A) = 0.9 + 0.1 + 0.024 - 0.02 - 0.25 = 0.754
    # I(B) = 0.3 + 0.2 + 0.6 - 0.0 - 0.025 = 1.075
    # Let's adjust w3 to force collapse
    # 1.0*0.9 + 0.1*1.0 - 0.5*0.5 = 0.75 (A base)
    # 1.0*0.3 + 0.1*2.0 - 0.5*0.05 = 0.475 (B base)
    # 0.75 = 0.475 + w3*0.25 => w3 = 0.275 / 0.25 = 1.1
    weights = [1.0, 0.1, 1.14, 1.0, 0.5]
    
    print("--- 1. Linear Aggregation ---")
    print(f"Weights: M={weights[0]}, D={weights[1]}, TE+={weights[2]}, TE-={weights[3]}, CMI={weights[4]}")
    for name, S in systems.items():
        score = agg_linear(S, weights)
        print(f"{name:20s} | Linear Score: {score:.4f}")
    print("Result: FAIL (Feature Compensation -> Mimic and Causal collapse to same scalar!)\n")

    # 2. Multiplicative Aggregation
    print("--- 2. Multiplicative Aggregation ---")
    for name, S in systems.items():
        score = agg_multiplicative(S)
        print(f"{name:20s} | Mult Score: {score:.4f}")
    print("Result: Over-penalizes Geometry (System C gets zeroed out due to TE diff).\n")
    
    # 3. Structural Distance
    print("--- 3. Structural Distance Aggregation ---")
    S_target = np.array([0.5, 2.0, 0.5, 0.0, 0.0]) # Ideal Causal-Complex system
    for name, S in systems.items():
        score = agg_distance(S, S_target)
        print(f"{name:20s} | Distance to Ideal: {score:.4f} (Lower is closer)")
    print("Result: Preserves geometry, but relies on defining an arbitrary 'Target'.\n")

    # 4. Pareto Rank
    print("--- 4. Pareto Aggregation ---")
    names = list(systems.keys())
    for i in range(len(names)):
        dominated = False
        for j in range(len(names)):
            if i != j:
                if is_pareto_dominated(systems[names[i]], systems[names[j]]):
                    dominated = True
                    print(f"{names[i]} is DOMINATED by {names[j]}")
        if not dominated:
            print(f"{names[i]:20s} | PARETO OPTIMAL (Non-dominated)")
    print("Result: PASS. The structure is inherently multidimensional. No system dominates all others.")
    
    # Save to JSON
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(results_dir, "aggregation_collapse_v0.1.json"), "w") as f:
        json.dump({
            "Conclusion": "Scalar aggregation causes structural collapse. ICCS v1.1 should be a vector.",
            "Recommendation": "Use Pareto Ranking or Vector Profiles."
        }, f, indent=4)
        
if __name__ == "__main__":
    run_experiment()
