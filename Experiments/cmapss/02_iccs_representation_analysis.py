import os
import sys
import yaml
import csv
import pandas as pd
import numpy as np

# Import existing ICCS from v0.1
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from psf import ICCS

def apply_pca(X_mat, n_components=3):
    # X_mat is (T, D)
    # Center the data
    X_centered = X_mat - np.mean(X_mat, axis=0)
    # SVD
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    # Principal components
    PCs = np.dot(U, np.diag(S))
    return PCs[:, :n_components]

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, 'data', 'cmapss', 'FD001', 'train_FD001.txt')
    yaml_path = os.path.join(base_dir, 'Experiments', 'cmapss', 'selected_channels.yaml')
    
    out_dir = os.path.join(base_dir, 'Results', 'cmapss', 'csv')
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, 'cmapss_representation_iccs.csv')
    
    if not os.path.exists(data_path) or not os.path.exists(yaml_path):
        print("[!] Data or selected_channels.yaml not found.")
        return
        
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        
    x_chan = config['channels']['X']
    y_chan = config['channels']['Y']
    z_chan = config['channels']['Z']
    
    cols = ['unit', 'cycles', 'os1', 'os2', 'os3'] + [f's{i}' for i in range(1, 22)]
    df = pd.read_csv(data_path, sep=r'\s+', header=None, names=cols)
    
    units = df['unit'].unique()
    iccs = ICCS(max_k_memory=10, k_neighbors_mi=10, k_neighbors_id=10)
    
    results = []
    num_units_to_process = 20
    units_to_process = units[:num_units_to_process]
    
    print(f"\n--- Processing Representation Boundary ({len(units_to_process)} Engines) ---")
    
    for u in units_to_process:
        df_u = df[df['unit'] == u].copy()
        max_cycle = df_u['cycles'].max()
        df_u['relative_cycle'] = df_u['cycles'] / max_cycle
        
        phases = {
            'Early': df_u[(df_u['relative_cycle'] >= 0.0) & (df_u['relative_cycle'] <= 0.33)],
            'Late': df_u[(df_u['relative_cycle'] > 0.66) & (df_u['relative_cycle'] <= 1.0)]
        }
        
        for phase_name, df_phase in phases.items():
            if len(df_phase) < 30:
                continue
                
            X_arr = df_phase[x_chan].values
            Y_arr = df_phase[y_chan].values
            Z_arr = df_phase[z_chan].values
            
            # Combine into matrix
            raw_matrix = np.column_stack((X_arr, Y_arr, Z_arr))
            pcs = apply_pca(raw_matrix, n_components=3)
            
            reps = []
            # 1. Raw
            reps.append(('Raw', 3, X_arr, Y_arr, Z_arr))
            
            # 2. Rolling Features
            roll_X = pd.Series(X_arr).rolling(window=10, min_periods=1, center=False).mean().values
            roll_Y = pd.Series(Y_arr).rolling(window=10, min_periods=1, center=False).mean().values
            roll_Z = pd.Series(Z_arr).rolling(window=10, min_periods=1, center=False).mean().values
            reps.append(('Rolling', 3, roll_X, roll_Y, roll_Z))
            
            # 3. PCA-2
            reps.append(('PCA-2', 2, pcs[:, 0], pcs[:, 1], None))
            
            # 4. PCA-1
            reps.append(('PCA-1', 1, pcs[:, 0], None, None))
            
            for rep_name, dim, X_in, Y_in, Z_in in reps:
                try:
                    # Pass a multivariate X so D_local measures the full dimensionality
                    # since ICCS uses X_geom = X and then takes X[:, 0] for the rest.
                    if dim == 3:
                        X_multi = np.column_stack((X_in, Y_in, Z_in))
                        prof = iccs.fit(X_multi, Y_in, Z_in)
                        te_f, te_r, cmi = prof['TE_forward'], prof['TE_reverse'], prof['CMI']
                    elif dim == 2:
                        X_multi = np.column_stack((X_in, Y_in))
                        prof = iccs.fit(X_multi, Y_in, None)
                        te_f, te_r, cmi = prof['TE_forward'], prof['TE_reverse'], np.nan
                    else:
                        prof = iccs.fit(X_in, None, None)
                        te_f, te_r, cmi = np.nan, np.nan, np.nan
                        
                    results.append({
                        'engine': u,
                        'phase': phase_name,
                        'representation': rep_name,
                        'dim': dim,
                        'M': prof['M'],
                        'D_local': prof['D_local'],
                        'TE_forward': te_f,
                        'TE_reverse': te_r,
                        'CMI': cmi
                    })
                except Exception as e:
                    print(f"  [!] Failed on {u}-{phase_name}-{rep_name}: {e}")
                    
    keys = ['engine', 'phase', 'representation', 'dim', 'M', 'D_local', 'TE_forward', 'TE_reverse', 'CMI']
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n[+] ICCS Representation Analysis Complete. Results saved to {out_csv}")

if __name__ == '__main__':
    main()
