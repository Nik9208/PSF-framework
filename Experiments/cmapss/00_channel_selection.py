import os
import yaml
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, 'data', 'cmapss', 'FD001', 'train_FD001.txt')
    out_yaml = os.path.join(base_dir, 'Experiments', 'cmapss', 'selected_channels.yaml')
    
    if not os.path.exists(data_path):
        print(f"[!] Data file not found: {data_path}")
        print("    Please ensure the C-MAPSS FD001 dataset is placed in the data directory.")
        return

    # Load C-MAPSS FD001
    # Columns: unit_nr, time_cycles, os_1, os_2, os_3, s_1 to s_21
    cols = ['unit', 'cycles', 'os1', 'os2', 'os3'] + [f's{i}' for i in range(1, 22)]
    df = pd.read_csv(data_path, sep=r'\s+', header=None, names=cols)
    
    sensor_cols = [f's{i}' for i in range(1, 22)]
    df_sensors = df[sensor_cols]
    
    # 1. Variance Filtering
    print("--- 1. Variance Filtering ---")
    variances = df_sensors.var()
    var_threshold = 1e-5
    active_sensors = variances[variances > var_threshold].index.tolist()
    dropped_sensors = set(sensor_cols) - set(active_sensors)
    
    print(f"Dropped flat sensors: {list(dropped_sensors)}")
    print(f"Active sensors ({len(active_sensors)}): {active_sensors}")
    
    if len(active_sensors) < 3:
        print("[!] Not enough active sensors for ICCS analysis.")
        return
        
    df_active = df_sensors[active_sensors]
    
    # 2. Redundancy Reduction via Clustering
    print("\n--- 2. Redundancy Reduction ---")
    np.random.seed(42) # Seed for reproducibility
    # Compute Spearman rank correlation
    corr_matrix, _ = spearmanr(df_active)
    # Convert to distance matrix: D = 1 - |corr|
    dist_matrix = 1 - np.abs(corr_matrix)
    # Ensure symmetry and zero diagonal
    np.fill_diagonal(dist_matrix, 0)
    condensed_dist = squareform(dist_matrix, checks=False)
    
    # Complete hierarchical clustering (valid for non-Euclidean distance)
    Z = linkage(condensed_dist, method='complete')
    
    # We want to extract 3 distinct physical clusters for X, Y, Z
    k_clusters = 3
    labels = fcluster(Z, k_clusters, criterion='maxclust')
    
    clusters = {1: [], 2: [], 3: []}
    for i, sensor in enumerate(active_sensors):
        clusters[labels[i]].append(sensor)
        
    for k, v in clusters.items():
        print(f"Cluster {k}: {v}")
        
    # 3. Representative Selection
    print("\n--- 3. Channel Selection ---")
    selected = {}
    axes = ['X', 'Y', 'Z']
    
    for i, axis in enumerate(axes):
        if i >= len(clusters):
            break
        c_id = i + 1
        cluster_sensors = clusters[c_id]
        
        # representative = sensor with highest variance
        rep = max(cluster_sensors, key=lambda s: variances[s])
        selected[axis] = rep
        print(f"{axis} assigned to {rep} (from Cluster {c_id})")
        
    # Save to YAML
    output_data = {
        'channels': selected,
        'selection_method': {
            'variance_filter': True,
            'variance_threshold': var_threshold,
            'clustering': 'Spearman Rank + Complete Linkage',
            'uses_rul': False,
            'manual_override': False
        }
    }
    
    with open(out_yaml, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False)
        
    print(f"\n[+] Protocol complete. Configuration saved to: {out_yaml}")

if __name__ == '__main__':
    main()
