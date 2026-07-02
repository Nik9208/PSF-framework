import os
import json
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Simple ICCS Pipeline Proxy for Raw Timeseries
class RawICCSPipeline:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        
    def fit_predict(self, X):
        if X.shape[1] < 3:
            # Embed using delay embedding if 1D
            if X.shape[1] == 1:
                delay = 1
                X_emb = np.column_stack([X[:-2*delay], X[delay:-delay], X[2*delay:]])
            else:
                X_emb = X
        else:
            X_emb = X
            
        X_scaled = StandardScaler().fit_transform(X_emb)
        pca = PCA(n_components=min(3, X_scaled.shape[1]))
        X_pca = pca.fit_transform(X_scaled)
        
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        labels = kmeans.fit_predict(X_pca)
        return labels

def generate_datasets():
    datasets = {}
    n = 1000
    
    # 1. Gaussian Noise
    datasets["Gaussian Noise"] = np.random.randn(n, 1)
    
    # 2. Random Walk
    datasets["Random Walk"] = np.cumsum(np.random.randn(n)).reshape(-1, 1)
    
    # 3. Logistic Map (Stable r=3.2)
    x_stable = np.zeros(n)
    x_stable[0] = 0.5
    for i in range(1, n):
        x_stable[i] = 3.2 * x_stable[i-1] * (1 - x_stable[i-1])
    datasets["Logistic (Stable)"] = x_stable.reshape(-1, 1)
    
    # 4. Logistic Map (Chaotic r=3.9)
    x_chaos = np.zeros(n)
    x_chaos[0] = 0.5
    for i in range(1, n):
        x_chaos[i] = 3.9 * x_chaos[i-1] * (1 - x_chaos[i-1])
    datasets["Logistic (Chaos)"] = x_chaos.reshape(-1, 1)
    
    # 5. Lorenz System
    dt = 0.01
    x, y, z = 1.0, 1.0, 1.0
    out = []
    for _ in range(n):
        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 2.667 * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        out.append([x, y, z])
    datasets["Lorenz"] = np.array(out)
    
    # 6. Shuffled Lorenz
    lorenz_shuffled = datasets["Lorenz"].copy()
    np.random.shuffle(lorenz_shuffled)
    datasets["Shuffled Lorenz"] = lorenz_shuffled

    return datasets

def compute_metrics(labels):
    # Unique clusters used
    n_clusters = len(np.unique(labels))
    
    # Stability
    changes = np.sum(np.diff(labels) != 0)
    stability = 1.0 / (1.0 + changes)
    
    # Entropy of transitions
    transitions = zip(labels[:-1], labels[1:])
    counts = Counter(transitions)
    total = sum(counts.values())
    probs = [c/total for c in counts.values()]
    entropy = -sum(p * np.log2(p) for p in probs)
    
    return n_clusters, stability, entropy

def run_harness():
    datasets = generate_datasets()
    pipeline = RawICCSPipeline(n_clusters=3)
    
    print("=== ICCS DEBUG HARNESS RESULTS ===")
    print(f"{'Dataset':<20} | {'Clusters':<8} | {'Stability':<10} | {'Trans. Entropy':<15}")
    print("-" * 65)
    
    results = []
    for name, X in datasets.items():
        labels = pipeline.fit_predict(X)
        n_c, stab, ent = compute_metrics(labels)
        print(f"{name:<20} | {n_c:<8} | {stab:<10.4f} | {ent:<15.4f}")
        
        results.append({
            "Dataset": name,
            "Clusters": n_c,
            "Stability": stab,
            "Entropy": ent
        })
        
    df = pd.DataFrame(results)
    df.to_csv("debug_harness_results.csv", index=False)
    
if __name__ == "__main__":
    run_harness()
