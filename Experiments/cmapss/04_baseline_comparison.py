import os
import pandas as pd
import numpy as np
import yaml
from scipy.stats import entropy
from sklearn.feature_selection import mutual_info_regression
from sklearn.decomposition import PCA

def compute_histogram_entropy(signal, bins=30):
    """Compute Shannon entropy using a simple histogram approach."""
    # Add small noise to avoid identical min/max if constant
    if np.var(signal) < 1e-9:
        return 0.0
    hist, _ = np.histogram(signal, bins=bins, density=True)
    # Filter out zero probabilities
    hist = hist[hist > 0]
    return entropy(hist)

def compute_knn_mi(x, y):
    """Compute continuous mutual information using k-NN estimator."""
    if np.var(x) < 1e-9 or np.var(y) < 1e-9:
        return 0.0
    # mutual_info_regression expects 2D array for X and 1D for y
    mi = mutual_info_regression(x.reshape(-1, 1), y, random_state=42)
    return mi[0]

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, 'data', 'cmapss', 'FD001', 'train_FD001.txt')
    yaml_path = os.path.join(base_dir, 'Experiments', 'cmapss', 'selected_channels.yaml')
    
    out_dir = os.path.join(base_dir, 'Results', 'cmapss', 'csv')
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, 'cmapss_baseline_comparison.csv')
    
    if not os.path.exists(data_path) or not os.path.exists(yaml_path):
        print("[!] Data or selected_channels.yaml not found.")
        return
        
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        channels = config.get('channels', {})
        ch_x = channels.get('X')
        ch_y = channels.get('Y')
        ch_z = channels.get('Z')
        
    print(f"[*] Baseline evaluation using channels: X={ch_x}, Y={ch_y}, Z={ch_z}")
    
    columns = ['engine', 'cycle', 'op1', 'op2', 'op3'] + [f's{i}' for i in range(1, 22)]
    df = pd.read_csv(data_path, sep=r'\s+', header=None, names=columns)
    
    engines = df['engine'].unique()[:20]
    
    results = []
    
    for eng in engines:
        eng_data = df[df['engine'] == eng].copy()
        max_cycle = eng_data['cycle'].max()
        
        # Split into Early (0-33%) and Late (66-100%)
        early_data = eng_data[eng_data['cycle'] <= int(max_cycle * 0.33)]
        late_data = eng_data[eng_data['cycle'] >= int(max_cycle * 0.66)]
        
        phases = {'Early': early_data, 'Late': late_data}
        
        for phase_name, data in phases.items():
            if len(data) < 30:
                print(f"[!] Engine {eng} phase {phase_name} has < 30 samples. Skipping.")
                continue
                
            x_raw = data[ch_x].values
            y_raw = data[ch_y].values
            z_raw = data[ch_z].values
            
            # Baseline 1: Scalar Variance
            var_x = np.var(x_raw)
            var_y = np.var(y_raw)
            var_z = np.var(z_raw)
            
            # Baseline 2: Correlation (absolute Pearson)
            corr_xy = np.abs(np.corrcoef(x_raw, y_raw)[0, 1])
            corr_xz = np.abs(np.corrcoef(x_raw, z_raw)[0, 1])
            if np.isnan(corr_xy): corr_xy = 0.0
            if np.isnan(corr_xz): corr_xz = 0.0
            
            # Baseline 3: Entropy (Histogram, bins=30)
            h_x = compute_histogram_entropy(x_raw, bins=30)
            h_y = compute_histogram_entropy(y_raw, bins=30)
            h_z = compute_histogram_entropy(z_raw, bins=30)
            
            # Baseline 4: MI (k-NN)
            mi_xy = compute_knn_mi(x_raw, y_raw)
            mi_xz = compute_knn_mi(x_raw, z_raw)
            
            # Baseline 5: PCA Latent (Explained Variance Ratio)
            # Stack data
            X_stack = np.vstack([x_raw, y_raw, z_raw]).T
            # Standardize before PCA (standard practice)
            stds = np.std(X_stack, axis=0)
            stds[stds < 1e-9] = 1e-9
            X_norm = (X_stack - np.mean(X_stack, axis=0)) / stds
            
            pca = PCA()
            pca.fit(X_norm)
            
            # Pad with zeros if intrinsic dim < 3 due to constant features
            evr = list(pca.explained_variance_ratio_)
            while len(evr) < 3:
                evr.append(0.0)
                
            pca_1_var = evr[0]
            pca_2_var = evr[0] + evr[1]
            
            results.append({
                'engine': eng,
                'phase': phase_name,
                'var_x': var_x,
                'var_y': var_y,
                'var_z': var_z,
                'corr_xy': corr_xy,
                'corr_xz': corr_xz,
                'h_x': h_x,
                'h_y': h_y,
                'h_z': h_z,
                'mi_xy': mi_xy,
                'mi_xz': mi_xz,
                'pca_1_var_ratio': pca_1_var,
                'pca_2_var_ratio': pca_2_var
            })
            
    df_res = pd.DataFrame(results)
    df_res.to_csv(out_csv, index=False)
    print(f"[*] Baseline comparison saved to {out_csv}")
    
    # Quick print of aggregated results
    agg = df_res.groupby('phase').mean()
    print("\n[+] Aggregated Results (Mean):")
    print(agg[['var_x', 'corr_xy', 'h_x', 'mi_xy', 'pca_1_var_ratio', 'pca_2_var_ratio']])

if __name__ == '__main__':
    main()
