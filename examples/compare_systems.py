import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
from psf import ICCS

def generate_causal_system(steps=2000, coupling=0.5):
    # X -> Y
    Z = np.random.randn(steps) # Unrelated Z for structural symmetry
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        X[t] = 0.5 * X[t-1] + np.random.randn()
        Y[t] = 0.5 * Y[t-1] + coupling * X[t-1] + np.random.randn()
    return X, Y, Z

def generate_mimic_system(steps=2000, coupling=0.5):
    # Predictive mimic (Independent harmonic temporal structure)
    # coupling acts inversely on noise to match MI
    noise = max(0.01, 1.5 - coupling)
    t = np.arange(steps)
    X = np.sin(0.1 * t) + np.random.randn(steps) * noise
    Y = np.sin(0.1 * t + np.pi/4) + np.random.randn(steps) * noise
    Z = np.random.randn(steps)
    return X, Y, Z

if __name__ == "__main__":
    print("Generating Systems...")
    X_causal, Y_causal, Z_causal = generate_causal_system(steps=2000, coupling=0.8)
    # Tune mimic coupling to roughly match the base predictive MI
    X_mimic, Y_mimic, Z_mimic = generate_mimic_system(steps=2000, coupling=1.35)
    
    print("Computing ICCS Profiles...")
    iccs = ICCS()
    prof_causal = iccs.fit(X_causal, Y_causal, Z_causal)
    prof_mimic = iccs.fit(X_mimic, Y_mimic, Z_mimic)
    
    print("\nBoundary Validation Protocol (BVP) Demonstration")
    print("Comparing structurally distinct systems that may exhibit similar raw predictive power.\n")
    
    print("System              M      D      TE+     TE-    CMI")
    print("-" * 55)
    
    def print_row(name, p):
        print(f"{name:<18} {p['M']:.2f}    {p['D_local']:.2f}    {p['TE_forward']:.2f}    {p['TE_reverse']:.2f}    {p['CMI']:.2f}")

    print_row("Causal (X->Y)", prof_causal)
    print_row("Mimic (Harmonic)", prof_mimic)
    
    # ---------------------------------------------------------
    # Visual Output (Grouped Bar Chart)
    # ---------------------------------------------------------
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nNote: matplotlib not found. Skipping plot generation.")
        sys.exit(0)
        
    labels = ['M', 'D_local', 'TE+', 'TE-', 'CMI']
    causal_vals = [prof_causal['M'], prof_causal['D_local'], prof_causal['TE_forward'], prof_causal['TE_reverse'], prof_causal['CMI']]
    mimic_vals = [prof_mimic['M'], prof_mimic['D_local'], prof_mimic['TE_forward'], prof_mimic['TE_reverse'], prof_mimic['CMI']]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, causal_vals, width, label='Causal (X->Y)')
    rects2 = ax.bar(x + width/2, mimic_vals, width, label='Mimic (Harmonic)')
    
    ax.set_ylabel('Score / Value')
    ax.set_title('Structural Feature Space (ICCS) Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), "compare_systems_plot.png")
    plt.savefig(plot_path)
    print(f"\nSaved visualization to {plot_path}")
