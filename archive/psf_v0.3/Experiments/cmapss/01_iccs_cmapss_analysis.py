import os
import sys
import yaml
import csv
import pandas as pd
import numpy as np

# Import existing ICCS from v0.1
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from psf import ICCS

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, 'data', 'cmapss', 'FD001', 'train_FD001.txt')
    yaml_path = os.path.join(base_dir, 'Experiments', 'cmapss', 'selected_channels.yaml')
    
    out_dir = os.path.join(base_dir, 'Results', 'cmapss', 'csv')
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, 'cmapss_temporal_iccs.csv')
    
    if not os.path.exists(data_path) or not os.path.exists(yaml_path):
        print("[!] Data or selected_channels.yaml not found.")
        return
        
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        
    x_chan = config['channels']['X']
    y_chan = config['channels']['Y']
    z_chan = config['channels']['Z']
    
    print(f"Loaded channels - X: {x_chan}, Y: {y_chan}, Z: {z_chan}")
    
    cols = ['unit', 'cycles', 'os1', 'os2', 'os3'] + [f's{i}' for i in range(1, 22)]
    df = pd.read_csv(data_path, sep=r'\s+', header=None, names=cols)
    
    units = df['unit'].unique()
    
    # We will instantiate ICCS once.
    # Note: K_neighbors could be tweaked, but we stick to the default robust values.
    # For small windows (e.g. 60 points), k=10 might be slightly large for ID, but we keep it fixed to avoid manual tweaking.
    iccs = ICCS(max_k_memory=10, k_neighbors_mi=10, k_neighbors_id=10)
    
    results = []
    
    # Process the first 20 units to keep execution time reasonable for the first validation pass, 
    # or all 100 if we want the full dataset. Let's do 20 for rapid empirical validation.
    num_units_to_process = 20
    units_to_process = units[:num_units_to_process]
    
    print(f"\n--- Processing {len(units_to_process)} Engines ---")
    
    for u in units_to_process:
        df_u = df[df['unit'] == u].copy()
        max_cycle = df_u['cycles'].max()
        df_u['relative_cycle'] = df_u['cycles'] / max_cycle
        
        phases = {
            'Early': df_u[(df_u['relative_cycle'] >= 0.0) & (df_u['relative_cycle'] <= 0.33)],
            'Middle': df_u[(df_u['relative_cycle'] > 0.33) & (df_u['relative_cycle'] <= 0.66)],
            'Late': df_u[(df_u['relative_cycle'] > 0.66) & (df_u['relative_cycle'] <= 1.0)]
        }
        
        print(f"Engine {u} (Max cycles: {max_cycle})")
        
        for phase_name, df_phase in phases.items():
            n_samples = len(df_phase)
            if n_samples < 30:
                print(f"  [!] Phase {phase_name} has too few samples ({n_samples} < 30). Skipping.")
                continue
                
            X_arr = df_phase[x_chan].values
            Y_arr = df_phase[y_chan].values
            Z_arr = df_phase[z_chan].values
            
            # Baseline: Scalar Variances
            var_X = np.var(X_arr)
            var_Y = np.var(Y_arr)
            var_Z = np.var(Z_arr)
            scalar_var_sum = var_X + var_Y + var_Z
            
            # Use strictly the existing ICCS implementation
            try:
                prof = iccs.fit(X_arr, Y_arr, Z_arr)
                
                results.append({
                    'engine': u,
                    'phase': phase_name,
                    'M': prof['M'],
                    'D_local': prof['D_local'],
                    'TE_forward': prof['TE_forward'],
                    'TE_reverse': prof['TE_reverse'],
                    'CMI': prof['CMI'],
                    'scalar_var_sum': scalar_var_sum
                })
            except Exception as e:
                print(f"  [!] Failed on {phase_name}: {e}")
                
    # Save Results
    keys = ['engine', 'phase', 'M', 'D_local', 'TE_forward', 'TE_reverse', 'CMI', 'scalar_var_sum']
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n[+] ICCS Temporal Analysis Complete. Results saved to {out_csv}")

if __name__ == '__main__':
    main()
