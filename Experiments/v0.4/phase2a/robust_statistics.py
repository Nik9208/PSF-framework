import os
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import permutation_test

def cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    sp = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / dof)
    if sp == 0: return np.nan
    return abs(np.mean(x) - np.mean(y)) / sp

def bootstrap_cohens_d(x, y, n_resamples=1000):
    ds = []
    nx, ny = len(x), len(y)
    for _ in range(n_resamples):
        xb = np.random.choice(x, size=nx, replace=True)
        yb = np.random.choice(y, size=ny, replace=True)
        ds.append(cohens_d(xb, yb))
    return np.percentile(ds, [2.5, 97.5])

def overlap_coefficient(x, y, bins=50):
    min_val = min(np.min(x), np.min(y))
    max_val = max(np.max(x), np.max(y))
    if min_val == max_val: return 1.0
    hist_x, _ = np.histogram(x, bins=bins, range=(min_val, max_val), density=True)
    hist_y, _ = np.histogram(y, bins=bins, range=(min_val, max_val), density=True)
    bin_width = (max_val - min_val) / bins
    return np.sum(np.minimum(hist_x, hist_y)) * bin_width

def bootstrap_roc_auc(x, y, n_resamples=1000):
    aucs = []
    labels = np.concatenate([np.zeros(len(x)), np.ones(len(y))])
    nx = len(x)
    for _ in range(n_resamples):
        xb = np.random.choice(x, size=len(x), replace=True)
        yb = np.random.choice(y, size=len(y), replace=True)
        lbls = np.concatenate([np.zeros(len(xb)), np.ones(len(yb))])
        scrs = np.concatenate([xb, yb])
        # Only compute if we have both classes
        if len(np.unique(lbls)) > 1:
            auc = roc_auc_score(lbls, scrs)
            aucs.append(max(auc, 1.0 - auc))
    if len(aucs) == 0: return np.nan, np.nan
    return np.percentile(aucs, [2.5, 97.5])

def perm_test_diff(x, y):
    def statistic(x, y, axis):
        return np.mean(x, axis=axis) - np.mean(y, axis=axis)
    res = permutation_test((x, y), statistic, n_resamples=1000, alternative='two-sided')
    return res.pvalue

RAW_DIR = os.path.join(os.path.dirname(__file__), 'results', 'raw')
raw_file = os.path.join(RAW_DIR, "phase2a_raw.csv")

if not os.path.exists(raw_file):
    print("Raw data not found. Please run the lab first.")
    exit(1)

df = pd.read_csv(raw_file)
df = df.dropna(subset=['D_local'])

pairs = [
    ('gaussian_white_noise', 'pink_noise', 'White-Pink'),
    ('gaussian_white_noise', 'ar1_05', 'White-AR1_05'),
    ('gaussian_white_noise', 'ar1_09', 'White-AR1_09'),
    ('ar1_09', 'pink_noise', 'AR1_09-Pink'),
    ('ar1_09', 'lorenz', 'AR1_09-Lorenz'),
    ('pink_noise', 'lorenz', 'Pink-Lorenz'),
    ('gaussian_white_noise', 'lorenz', 'White-Lorenz')
]

results = []

for m in df['m'].unique():
    for tau in df['tau'].unique():
        if pd.isna(tau):
            subset = df[(df['m'] == m) & (df['tau'].isna())]
        else:
            subset = df[(df['m'] == m) & (df['tau'] == tau)]
            
        for sig1, sig2, label in pairs:
            x = subset[subset['Signal'] == sig1]['D_local'].values
            y = subset[subset['Signal'] == sig2]['D_local'].values
            
            if len(x) > 0 and len(y) > 0:
                d = cohens_d(x, y)
                d_ci = bootstrap_cohens_d(x, y)
                ovl = overlap_coefficient(x, y)
                
                labels = np.concatenate([np.zeros(len(x)), np.ones(len(y))])
                scores = np.concatenate([x, y])
                auc_val = roc_auc_score(labels, scores)
                auc = max(auc_val, 1.0 - auc_val)
                auc_ci = bootstrap_roc_auc(x, y)
                
                pval = perm_test_diff(x, y)
                
                results.append({
                    'm': m,
                    'tau': tau if not pd.isna(tau) else 'raw',
                    'Pair': label,
                    'd': d,
                    'd_ci_lower': d_ci[0],
                    'd_ci_upper': d_ci[1],
                    'Overlap': ovl,
                    'AUC': auc,
                    'AUC_ci_lower': auc_ci[0],
                    'AUC_ci_upper': auc_ci[1],
                    'P_val': pval
                })

res_df = pd.DataFrame(results)
out_file = os.path.join(os.path.dirname(__file__), 'results', 'tables', 'robust_statistics.csv')
res_df.to_csv(out_file, index=False)
print(f"Robust statistics saved to {out_file}")
