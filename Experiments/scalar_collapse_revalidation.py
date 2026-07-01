import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_profile(row):
    return np.array([float(row['M']), float(row['D_local']), float(row['TE_forward']), float(row['CMI'])])

def calc_scalars(S, S_ref=None):
    f1 = np.linalg.norm(S)              # L2 Norm
    f2 = np.sum(S)                      # Sum
    f3 = np.linalg.norm(S - S_ref) if S_ref is not None else 0.0 # Distance to ref
    return f1, f2, f3

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_path = os.path.join(base_dir, 'Results', 'robustness_raw.csv')
    out_csv = os.path.join(base_dir, 'paper', 'tables', 'scalar_collapse.csv')
    out_fig = os.path.join(base_dir, 'paper', 'figures', 'fig5_scalar_collapse.png')
    
    with open(raw_path, 'r') as f:
        reader = csv.DictReader(f)
        results = list(reader)
        
    exp1 = [r for r in results if r['exp'] == 'Noise' and r['k'] == '10']
    noises = sorted(list(set(float(r['noise']) for r in exp1)))
    
    # Get reference profile (Causal at noise 0)
    ref_row = next(r for r in exp1 if float(r['noise']) == 0.0 and r['system'] == 'Causal')
    S_ref = get_profile(ref_row)
    
    table_data = []
    
    metrics = {'L2': [], 'Sum': [], 'DistRef': []}
    
    for n in noises:
        c_row = next(r for r in exp1 if float(r['noise']) == n and r['system'] == 'Causal')
        m_row = next(r for r in exp1 if float(r['noise']) == n and r['system'] == 'Mimic')
        
        S_c = get_profile(c_row)
        S_m = get_profile(m_row)
        
        f1_c, f2_c, f3_c = calc_scalars(S_c, S_ref)
        f1_m, f2_m, f3_m = calc_scalars(S_m, S_ref)
        
        # Relative gaps for scalars
        gap_f1 = abs(f1_c - f1_m) / (abs(f1_c) + abs(f1_m) + 1e-6)
        gap_f2 = abs(f2_c - f2_m) / (abs(f2_c) + abs(f2_m) + 1e-6)
        gap_f3 = abs(f3_c - f3_m) / (abs(f3_c) + abs(f3_m) + 1e-6)
        
        # Original BVP Vector Gap (from TE)
        te_c = float(c_row['TE_forward'])
        te_m = float(m_row['TE_forward'])
        gap_vector = abs(te_c - te_m) / (abs(te_c) + abs(te_m) + 1e-6)
        
        table_data.append({
            'Noise': n,
            'Vector_RelGap': gap_vector,
            'L2_RelGap': gap_f1,
            'Sum_RelGap': gap_f2,
            'DistRef_RelGap': gap_f3
        })
        
    # Save table
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Noise', 'Vector_RelGap', 'L2_RelGap', 'Sum_RelGap', 'DistRef_RelGap'])
        writer.writeheader()
        writer.writerows(table_data)
        
    # Plotting
    noises_arr = [d['Noise'] for d in table_data]
    vec_gaps = [d['Vector_RelGap'] for d in table_data]
    f1_gaps = [d['L2_RelGap'] for d in table_data]
    f2_gaps = [d['Sum_RelGap'] for d in table_data]
    f3_gaps = [d['DistRef_RelGap'] for d in table_data]
    
    plt.figure(figsize=(8, 6))
    plt.plot(noises_arr, vec_gaps, 'k-o', linewidth=2, label='Vector S(X) (BVP Separation)')
    plt.plot(noises_arr, f1_gaps, 'r--x', label='Scalar: $L_2$ Norm')
    plt.plot(noises_arr, f2_gaps, 'b--s', label='Scalar: Sum $\\Sigma S_i$')
    plt.plot(noises_arr, f3_gaps, 'g--^', label='Scalar: Distance to Ref $||S-S_{ref}||$')
    
    plt.axhline(0.1, color='gray', linestyle=':', label='Failure Threshold (0.1)')
    
    plt.title("Boundary Preservation: Vector vs Scalar Aggregation")
    plt.xlabel("Relative Gaussian Noise ($\\alpha$)")
    plt.ylabel("Relative Gap (Causal vs Mimic)")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(out_fig, dpi=300, bbox_inches='tight')
    print(f"Saved figure to {out_fig}")
    print(f"Saved table to {out_csv}")
    
    print("\nResults Analysis:")
    for d in table_data:
        print(f"Noise {d['Noise']:.2f} | Vector Gap: {d['Vector_RelGap']:.2f} | L2 Gap: {d['L2_RelGap']:.2f} | Sum Gap: {d['Sum_RelGap']:.2f} | DistRef Gap: {d['DistRef_RelGap']:.2f}")

if __name__ == '__main__':
    main()
