import os
import pandas as pd
import numpy as np

def pooled_std(s1, s2, n1=100, n2=100):
    return np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))

def cohens_d(m1, m2, s1, s2, n1=100, n2=100):
    sp = pooled_std(s1, s2, n1, n2)
    if sp == 0 or np.isnan(sp):
        return np.nan
    return abs(m1 - m2) / sp

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results', 'tables')
df = pd.read_csv(os.path.join(RESULTS_DIR, "phase2a_summary.csv"))

# Filter stochastic signals
df = df[df['Signal'].isin(['gaussian_white_noise', 'pink_noise', 'lorenz'])]

pairs = [
    ('gaussian_white_noise', 'lorenz', 'White-Lorenz'),
    ('gaussian_white_noise', 'pink_noise', 'White-Pink'),
    ('pink_noise', 'lorenz', 'Pink-Lorenz')
]

results = []

for m in df['m'].unique():
    for tau in df['tau'].dropna().unique():
        if pd.isna(tau):
            subset = df[(df['m'] == m) & (df['tau'].isna())]
        else:
            subset = df[(df['m'] == m) & (df['tau'] == tau)]
            
        for sig1, sig2, label in pairs:
            row1 = subset[subset['Signal'] == sig1]
            row2 = subset[subset['Signal'] == sig2]
            
            if not row1.empty and not row2.empty:
                m1 = row1['D_local_mean'].values[0]
                s1 = row1['D_local_std'].values[0]
                m2 = row2['D_local_mean'].values[0]
                s2 = row2['D_local_std'].values[0]
                
                d = cohens_d(m1, m2, s1, s2)
                results.append({
                    'm': m,
                    'tau': tau if not pd.isna(tau) else 'raw',
                    'Pair': label,
                    'Cohens_d': d
                })

# Baseline (Raw)
subset_raw = df[(df['m'] == 1)]
for sig1, sig2, label in pairs:
    row1 = subset_raw[subset_raw['Signal'] == sig1]
    row2 = subset_raw[subset_raw['Signal'] == sig2]
    if not row1.empty and not row2.empty:
        m1 = row1['D_local_mean'].values[0]
        s1 = row1['D_local_std'].values[0]
        m2 = row2['D_local_mean'].values[0]
        s2 = row2['D_local_std'].values[0]
        d = cohens_d(m1, m2, s1, s2)
        results.append({
            'm': 1,
            'tau': 'raw',
            'Pair': label,
            'Cohens_d': d
        })

res_df = pd.DataFrame(results).drop_duplicates()
print(res_df.pivot(index=['m', 'tau'], columns='Pair', values='Cohens_d').round(2))
