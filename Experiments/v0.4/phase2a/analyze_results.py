import os
import pandas as pd

CSV_PATH = os.path.join(os.path.dirname(__file__), 'results', 'tables', 'robust_statistics.csv')
df = pd.read_csv(CSV_PATH)

def analyze_endpoints():
    print("=== PHASE 2A PRIMARY ENDPOINT ANALYSIS ===")
    
    # Let's check stability across m > 1 for Lorenz vs White
    lorenz_vs_white = df[df['Pair'] == 'White-Lorenz']
    print("\nWhite vs Lorenz Separation:")
    print(lorenz_vs_white[['m', 'tau', 'AUC', 'd', 'Overlap', 'P_val']].to_string(index=False))

    # Let's check Pink vs Lorenz
    lorenz_vs_pink = df[df['Pair'] == 'Pink-Lorenz']
    print("\nPink vs Lorenz Separation:")
    print(lorenz_vs_pink[['m', 'tau', 'AUC', 'd', 'Overlap', 'P_val']].to_string(index=False))

    # Check AR(1) 0.9 vs Lorenz
    lorenz_vs_ar1 = df[df['Pair'] == 'AR1_09-Lorenz']
    print("\nAR1(0.9) vs Lorenz Separation:")
    print(lorenz_vs_ar1[['m', 'tau', 'AUC', 'd', 'Overlap', 'P_val']].to_string(index=False))

    # Check White vs Pink (should NOT separate significantly if geometry is just random noise)
    white_vs_pink = df[df['Pair'] == 'White-Pink']
    print("\nWhite vs Pink Separation:")
    print(white_vs_pink[['m', 'tau', 'AUC', 'd', 'Overlap', 'P_val']].to_string(index=False))

    # Check White vs AR1_09
    white_vs_ar1 = df[df['Pair'] == 'White-AR1_09']
    print("\nWhite vs AR1_09 Separation:")
    print(white_vs_ar1[['m', 'tau', 'AUC', 'd', 'Overlap', 'P_val']].to_string(index=False))

if __name__ == '__main__':
    analyze_endpoints()
