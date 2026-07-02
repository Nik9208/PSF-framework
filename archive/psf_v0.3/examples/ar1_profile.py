import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
from psf import ICCS

def generate_ar1(a=0.9, noise_std=1.0, steps=2000):
    X = np.zeros(steps)
    X[0] = np.random.randn() * noise_std
    for i in range(1, steps):
        X[i] = a * X[i-1] + np.random.randn() * noise_std
    return X

if __name__ == "__main__":
    print("Generating AR(1) process data (a=0.9)...")
    X = generate_ar1(steps=2000)
    
    print("Computing ICCS Profile...")
    profile = ICCS(max_k_memory=10, k_neighbors_id=10).fit(X)
    
    print("\nAR(1) ICCS Profile:")
    print(f"Memory M(k):       {profile['M']:.4f}")
    print(f"Local Dim D:       {profile['D_local']:.4f}")
    print(f"Forward TE:        {profile['TE_forward']:.4f}")
    print(f"Reverse TE:        {profile['TE_reverse']:.4f}")
    print(f"CMI (Causal):      {profile['CMI']:.4f}")
