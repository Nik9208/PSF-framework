import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), 'results', 'raw')
raw_file = os.path.join(RAW_DIR, "phase2a_raw.csv")

if not os.path.exists(raw_file):
    print("Raw file not found!")
    exit(1)

df = pd.read_csv(raw_file)

print("=== DATA INTEGRITY CHECK ===\n")

# 1. Number of realizations
configs = df.groupby(['Signal', 'm', 'tau'], dropna=False).size()
invalid_configs = configs[configs != 100]
print(f"[Number of realizations]")
if len(invalid_configs) == 0:
    print("PASS: All configurations have exactly 100 realizations.")
else:
    print("FAIL: Some configurations do not have exactly 100 realizations:")
    print(invalid_configs)

# 2. Effective length
# Expected: N_eff = 1000 - (m-1)*tau (or 1000 for m=1)
def check_neff(row):
    m = row['m']
    tau = 1 if pd.isna(row['tau']) else row['tau']
    expected = 1000 if m == 1 else 1000 - (m - 1) * tau
    return row['N_eff'] == expected

n_eff_check = df.apply(check_neff, axis=1)
print(f"\n[Effective length]")
if n_eff_check.all():
    print("PASS: All N_eff values match expected formula.")
else:
    print("FAIL: Some N_eff values are incorrect.")
    print(df[~n_eff_check][['Signal', 'm', 'tau', 'N_eff']])

# 3. Missing values
missing_d = df['D_local'].isna().sum()
print(f"\n[Missing values]")
if missing_d == 0:
    print("PASS: No missing values for D_local.")
else:
    print(f"FAIL: Found {missing_d} missing values for D_local.")

# 4. Failed ICCS runs
if 'error' in df.columns:
    failed_runs = df['error'].notna().sum()
else:
    failed_runs = 0
    
print(f"\n[Failed ICCS runs]")
if failed_runs == 0:
    print("PASS: 0 failed ICCS runs.")
else:
    print(f"FAIL: {failed_runs} failed runs.")
    print(df[df['error'].notna()][['Signal', 'm', 'tau', 'error']].head())

print("\n=== SUMMARY STATISTICS ===")
summary = df.groupby(['Signal', 'm', 'tau'], dropna=False)['D_local'].agg(['mean', 'std']).round(4)
print(summary)
