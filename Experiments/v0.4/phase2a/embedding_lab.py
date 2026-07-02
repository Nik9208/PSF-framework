import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from signal_generators import generate_gaussian_white_noise, generate_pink_noise, generate_sine, generate_lorenz, generate_ar1
from run_iccs_embedded import run_iccs_embedded

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
TABLES_DIR = os.path.join(RESULTS_DIR, 'tables')
RAW_DIR = os.path.join(RESULTS_DIR, 'raw')
os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

N_POINTS = 1000
N_RUNS = 100

SIGNALS = {
    "gaussian_white_noise": {"func": generate_gaussian_white_noise, "stochastic": True},
    "pink_noise": {"func": generate_pink_noise, "stochastic": True},
    "ar1_05": {"func": lambda n, seed=None: generate_ar1(n, 0.5, seed), "stochastic": True},
    "ar1_09": {"func": lambda n, seed=None: generate_ar1(n, 0.9, seed), "stochastic": True},
    "lorenz": {"func": generate_lorenz, "stochastic": True}
}

PARAMS = [
    {"m": 1, "tau": 1}, # Baseline (tau is ignored)
]
for m in [2, 3, 4, 5]:
    for tau in [1, 5, 10]:
        PARAMS.append({"m": m, "tau": tau})

def calculate_mean_M(m_dict):
    if isinstance(m_dict, dict):
        vals = list(m_dict.values())
        return np.mean(vals) if len(vals) > 0 else np.nan
    elif isinstance(m_dict, (list, np.ndarray)):
        return np.mean(m_dict) if len(m_dict) > 0 else np.nan
    return float(m_dict)

def execute_lab():
    summary_data = []
    all_raw_results = []
    
    for name, config in SIGNALS.items():
        print(f"Testing {name}...")
        func = config["func"]
        is_stochastic = config["stochastic"]
        runs = N_RUNS if is_stochastic else 1
        
        for param in PARAMS:
            m = param["m"]
            tau = param["tau"]
            
            results = []
            for i in tqdm(range(runs), desc=f"m={m}, tau={tau}", leave=False):
                try:
                    sig = func(n=N_POINTS, seed=i) if is_stochastic else func(n=N_POINTS)
                    prof = run_iccs_embedded(sig, m, tau)
                    
                    n_eff = N_POINTS if m == 1 else N_POINTS - (m - 1) * tau
                    if "error" in prof:
                        res = {"Signal": name, "m": m, "tau": tau, "run": i, "N_eff": n_eff, "error": prof["error"], "M_mean": np.nan, "D_local": np.nan, "TE_fwd": np.nan}
                    else:
                        res = {
                            "Signal": name,
                            "m": m,
                            "tau": tau,
                            "run": i,
                            "N_eff": n_eff,
                            "M_mean": calculate_mean_M(prof["M"]), 
                            "D_local": float(prof["D_local"]), 
                            "TE_fwd": float(prof["TE_forward"])
                        }
                    results.append(res)
                    all_raw_results.append(res)
                except Exception as e:
                    res_err = {"Signal": name, "m": m, "tau": tau, "run": i, "N_eff": n_eff, "error": str(e), "M_mean": np.nan, "D_local": np.nan, "TE_fwd": np.nan}
                    results.append(res_err)
                    all_raw_results.append(res_err)
                    
            df = pd.DataFrame(results)
            if len(df) == 0: continue
            
            agg = {"Signal": name, "Runs": runs, "m": m, "tau": tau}
            for col in ["M_mean", "D_local", "TE_fwd"]:
                if col in df.columns:
                    valid_data = df[col].dropna()
                    agg[f"{col}_mean"] = valid_data.mean() if len(valid_data) > 0 else np.nan
                    if runs > 1:
                        std = valid_data.std()
                        ci = 1.96 * std / np.sqrt(len(valid_data)) if len(valid_data) > 0 else np.nan
                        agg[f"{col}_std"] = std
                        agg[f"{col}_ci95"] = ci
            summary_data.append(agg)

    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(TABLES_DIR, "phase2a_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    
    raw_df = pd.DataFrame(all_raw_results)
    raw_path = os.path.join(RAW_DIR, "phase2a_raw.csv")
    raw_df.to_csv(raw_path, index=False)
    
    print(f"\nPhase 2A lab complete. Summary saved to {summary_path}")
    print(f"Raw data saved to {raw_path}")

if __name__ == "__main__":
    execute_lab()
