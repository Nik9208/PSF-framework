import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    results_dir = os.path.join(base_dir, 'Results', 'cmapss')
    figures_dir = os.path.join(results_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. Temporal Boundary
    df_temp = pd.read_csv(os.path.join(results_dir, 'csv', 'cmapss_temporal_iccs.csv'))
    temp_agg = df_temp.groupby('phase')[['M', 'D_local', 'CMI']].mean().reindex(['Early', 'Middle', 'Late'])
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(temp_agg.index, temp_agg['M'], marker='o', color='red', linewidth=2)
    axes[0].set_title('Autoregressive Memory (M)')
    axes[0].grid(True)
    
    axes[1].plot(temp_agg.index, temp_agg['D_local'], marker='s', color='blue', linewidth=2)
    axes[1].set_title('Local Dimension (D_local)')
    axes[1].grid(True)
    
    axes[2].plot(temp_agg.index, temp_agg['CMI'], marker='^', color='green', linewidth=2)
    axes[2].set_title('Dependency Coupling (CMI)')
    axes[2].grid(True)
    
    plt.suptitle('Temporal Boundary: ICCS Component Evolution', y=1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '01_temporal_iccs.png'), bbox_inches='tight')
    plt.close()
    
    # 2. Representation Boundary
    df_rep = pd.read_csv(os.path.join(results_dir, 'csv', 'cmapss_representation_iccs.csv'))
    # Use Late phase for representation heatmap as it contains the strongest signals
    df_rep_late = df_rep[df_rep['phase'] == 'Late']
    
    rep_agg = df_rep_late.groupby('representation')[['M', 'D_local', 'TE_forward', 'CMI']].mean()
    rep_agg = rep_agg.reindex(['Raw', 'Rolling', 'PCA-2', 'PCA-1'])
    
    # Normalize each column by its max value to see relative preservation
    rep_norm = rep_agg / rep_agg.max()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(rep_norm.values, cmap='viridis', aspect='auto')
    
    # Add text annotations
    for i in range(rep_norm.shape[0]):
        for j in range(rep_norm.shape[1]):
            val = rep_agg.values[i, j]
            text_color = "white" if rep_norm.values[i, j] < 0.5 else "black"
            if not np.isnan(val):
                ax.text(j, i, f'{val:.3f}', ha="center", va="center", color=text_color)
            else:
                ax.text(j, i, 'NaN', ha="center", va="center", color=text_color)
                
    ax.set_xticks(np.arange(len(rep_norm.columns)))
    ax.set_yticks(np.arange(len(rep_norm.index)))
    ax.set_xticklabels(rep_norm.columns)
    ax.set_yticklabels(rep_norm.index)
    plt.colorbar(im, label='Normalized Magnitude')
    plt.title('Representation Boundary (Late Phase)')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '02_representation_boundary.png'), bbox_inches='tight')
    plt.close()
    
    # 3. Noise Boundary
    df_noise = pd.read_csv(os.path.join(results_dir, 'csv', 'cmapss_noise_iccs.csv'))
    df_noise_valid = df_noise[df_noise['valid'] == True]
    noise_agg = df_noise_valid.groupby(['phase', 'noise'])[['M', 'D_local', 'CMI']].mean().reset_index()
    
    late_noise = noise_agg[noise_agg['phase'] == 'Late'].sort_values('noise')
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    x_labels = [f"{int(n*100)}%" for n in late_noise['noise']]
    
    axes[0].plot(x_labels, late_noise['M'], marker='o', color='red', linewidth=2)
    axes[0].set_title('Memory Attenuation (M)')
    axes[0].set_xlabel('Relative Noise')
    axes[0].grid(True)
    
    axes[1].plot(x_labels, late_noise['D_local'], marker='s', color='blue', linewidth=2)
    axes[1].set_title('Geometric Stability (D_local)')
    axes[1].set_xlabel('Relative Noise')
    # Set y-lim slightly wider to show it's flat
    axes[1].set_ylim(2.5, 3.5)
    axes[1].grid(True)
    
    axes[2].plot(x_labels, late_noise['CMI'], marker='^', color='green', linewidth=2)
    axes[2].set_title('Dependency Persistence (CMI)')
    axes[2].set_xlabel('Relative Noise')
    axes[2].grid(True)
    
    plt.suptitle('Noise Boundary (Late Phase)', y=1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '03_noise_boundary.png'), bbox_inches='tight')
    plt.close()
    
    # 4. Normalized Component Plot (replaces radar chart)
    # Compare Early vs Late in Raw representation
    raw_agg = df_rep[df_rep['representation'] == 'Raw'].groupby('phase')[['M', 'D_local', 'TE_forward', 'CMI']].mean()
    
    # Normalize by the max of Early/Late
    max_vals = raw_agg.max()
    norm_agg = raw_agg / max_vals
    norm_agg = norm_agg.reindex(['Early', 'Late'])
    
    norm_agg.T.plot(kind='bar', figsize=(8, 5), color=['lightblue', 'salmon'])
    plt.title('Normalized ICCS Components (Early vs Late)')
    plt.ylabel('Relative Magnitude')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '04_component_normalized.png'), bbox_inches='tight')
    plt.close()
    
    print(f"[+] All figures generated in {figures_dir}")

if __name__ == '__main__':
    main()
