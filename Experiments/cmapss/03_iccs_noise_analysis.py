import os
import sys
import yaml
import csv
import pandas as pd
import numpy as np

# Import existing ICCS from v0.1
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from psf import ICCS

def apply_relative_noise(signal, noise_level, rng):
    if noise_level == 0.0:
        return signal
    sigma = np.std(signal)
    noise = rng.normal(0, noise_level, size=len(signal)) * sigma
    return signal + noise

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, 'data', 'cmapss', 'FD001', 'train_FD001.txt')
    yaml_path = os.path.join(base_dir, 'Experiments', 'cmapss', 'selected_channels.yaml')
    
    out_dir = os.path.join(base_dir, 'Results', 'cmapss', 'csv')
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, 'cmapss_noise_iccs.csv')
    
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
    
    noise_levels = [0.0, 0.05, 0.10, 0.20]
    repeats = 5
    
    print(f"\n--- Processing Noise Boundary ({len(units_to_process)} Engines, {repeats} repeats) ---")
    
    for u in units_to_process:
        df_u = df[df['unit'] == u].copy()
        max_cycle = df_u['cycles'].max()
        df_u['relative_cycle'] = df_u['cycles'] / max_cycle
        
        phases = {
            'Early': df_u[(df_u['relative_cycle'] >= 0.0) & (df_u['relative_cycle'] <= 0.33)],
            'Late': df_u[(df_u['relative_cycle'] > 0.66) & (df_u['relative_cycle'] <= 1.0)]
        }
        
        for phase_name, df_phase in phases.items():
            valid_phase = len(df_phase) >= 30
                
            X_raw = df_phase[x_chan].values if valid_phase else np.array([])
            Y_raw = df_phase[y_chan].values if valid_phase else np.array([])
            Z_raw = df_phase[z_chan].values if valid_phase else np.array([])
            
            for noise in noise_levels:
                num_reps = 1 if noise == 0.0 else repeats
                
                for rep in range(num_reps):
                    base_res = {
                        'engine': u,
                        'phase': phase_name,
                        'noise': noise,
                        'repeat': rep,
                        'M': np.nan, 'D_local': np.nan, 'TE_forward': np.nan, 'TE_reverse': np.nan, 'CMI': np.nan,
                        'valid': False
                    }
                    
                    if not valid_phase:
                        results.append(base_res)
                        continue
                        
                    # Fix seed for reproducibility but different for each repeat
                    seed = int(u * 10000 + (1 if phase_name == 'Early' else 2) * 1000 + noise * 100000 + rep)
                    rng = np.random.default_rng(seed)
                    
                    X_noisy = apply_relative_noise(X_raw, noise, rng)
                    Y_noisy = apply_relative_noise(Y_raw, noise, rng)
                    Z_noisy = apply_relative_noise(Z_raw, noise, rng)
                    
                    try:
                        X_multi = np.column_stack((X_noisy, Y_noisy, Z_noisy))
                        prof = iccs.fit(X_multi, Y_noisy, Z_noisy)
                        
                        base_res.update({
                            'M': prof['M'],
                            'D_local': prof['D_local'],
                            'TE_forward': prof['TE_forward'],
                            'TE_reverse': prof['TE_reverse'],
                            'CMI': prof['CMI'],
                            'valid': True
                        })
                    except Exception as e:
                        # Will record as valid=False and NaNs
                        pass
                        
                    results.append(base_res)
                    
    keys = ['engine', 'phase', 'noise', 'repeat', 'M', 'D_local', 'TE_forward', 'TE_reverse', 'CMI', 'valid']
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n[+] ICCS Noise Analysis Complete. Results saved to {out_csv}")

if __name__ == '__main__':
    main()
