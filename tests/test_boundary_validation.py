import sys
import os
import numpy as np

# Ensure tests can import the src module if not installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from psf import ICCS

def generate_causal_system(steps=1000):
    Z = np.random.randn(steps)
    X = np.zeros(steps)
    Y = np.zeros(steps)
    for t in range(1, steps):
        X[t] = 0.5 * X[t-1] + np.random.randn()
        Y[t] = 0.5 * Y[t-1] + 0.8 * X[t-1] + np.random.randn()
    return X, Y, Z

def generate_mimic_system(steps=1000):
    t = np.arange(steps)
    noise = 0.1
    X = np.sin(0.1 * t) + np.random.randn(steps) * noise
    Y = np.sin(0.1 * t + np.pi/4) + np.random.randn(steps) * noise
    Z = np.random.randn(steps)
    return X, Y, Z

def test_causal_boundary_separation():
    """
    Scientific Assertion:
    A valid causal descriptor (TE) must distinguish between an actually coupled system 
    and a predictively identical mimic (harmonic).
    """
    X_c, Y_c, Z_c = generate_causal_system(steps=1500)
    X_m, Y_m, Z_m = generate_mimic_system(steps=1500)
    
    iccs = ICCS(k_neighbors_mi=5)
    
    causal_prof = iccs.fit(X_c, Y_c, Z_c)
    mimic_prof = iccs.fit(X_m, Y_m, Z_m)
    
    # Assert relational properties, not hardcoded numbers
    threshold = 0.1
    assert (causal_prof['TE_forward'] - mimic_prof['TE_forward']) > threshold, \
        "Causal boundary failed: TE_forward did not reliably identify the true causal direction vs the mimic."

def test_representation_boundary():
    """
    Scientific Assertion:
    A valid structural geometry descriptor (D_local) must remain invariant under 
    benign bijective transformations (e.g., scaling + rotation).
    """
    steps = 1500
    # Generate a simple 2D spiral
    t = np.linspace(0, 10 * np.pi, steps)
    X_base = np.column_stack((t * np.cos(t), t * np.sin(t)))
    X_base += np.random.randn(steps, 2) * 0.1
    
    # Transform: Scale and Rotate
    theta = np.pi / 4
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    S = np.array([[2.0, 0.0], [0.0, 0.5]])
    
    X_transformed = (X_base @ S) @ R
    
    iccs = ICCS(k_neighbors_id=15)
    
    base_prof = iccs.fit(X_base)
    trans_prof = iccs.fit(X_transformed)
    
    # Assert stability under transformation (relative difference)
    rel_diff = abs(base_prof['D_local'] - trans_prof['D_local']) / base_prof['D_local']
    tolerance = 0.25
    assert rel_diff < tolerance, \
        f"Representation boundary failed: D_local relative shift {rel_diff:.2f} exceeded tolerance {tolerance}."

if __name__ == "__main__":
    test_causal_boundary_separation()
    test_representation_boundary()
    print("All scientific boundary invariant tests passed.")
