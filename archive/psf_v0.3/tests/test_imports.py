import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import numpy as np
from psf import ICCS

def test_iccs_runs():
    # Generate a simple test signal
    x = np.sin(np.linspace(0, 10, 100)) + np.random.randn(100) * 0.1
    
    # Run ICCS
    result = ICCS(max_k_memory=3, k_neighbors_mi=3, k_neighbors_id=3).fit(x)
    
    # Check that the main object works and returns the expected profile structure
    assert "M" in result
    assert "D_local" in result
    assert "TE_forward" in result
    assert "TE_reverse" in result
    assert "CMI" in result
    
    # Verify values are numeric
    for key in result.vector:
        assert isinstance(result[key], float)

if __name__ == "__main__":
    test_iccs_runs()
    print("Smoke test passed successfully!")
