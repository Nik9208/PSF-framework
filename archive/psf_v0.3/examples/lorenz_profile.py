import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
from scipy.integrate import odeint
from psf import ICCS

def lorenz_system(state, t, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def generate_lorenz(steps=2000, dt=0.01, skip=1000):
    t = np.arange(0, (steps + skip) * dt, dt)
    state0 = [1.0, 1.0, 1.0]
    traj = odeint(lorenz_system, state0, t)
    return traj[skip:, 0]

if __name__ == "__main__":
    print("Generating Lorenz attractor data (X coordinate)...")
    X = generate_lorenz(steps=2000)
    
    print("Computing ICCS Profile...")
    profile = ICCS(max_k_memory=10, k_neighbors_id=10).fit(X)
    
    print("\nLorenz ICCS Profile:")
    print(f"Memory M(k):       {profile['M']:.4f}")
    print(f"Local Dim D:       {profile['D_local']:.4f}")
    print(f"Forward TE:        {profile['TE_forward']:.4f}")
    print(f"Reverse TE:        {profile['TE_reverse']:.4f}")
    print(f"CMI (Causal):      {profile['CMI']:.4f}")
