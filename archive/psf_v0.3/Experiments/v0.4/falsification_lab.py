import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from signal_generators import *
from run_iccs import run_iccs
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
TABLES_DIR = os.path.join(RESULTS_DIR, 'tables')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
RAW_DIR = os.path.join(RESULTS_DIR, 'raw')

os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

N_POINTS = 1000
N_RUNS = 30 # Number of independent realizations for stochastic signals

SIGNALS = {
    "constant": {"func": generate_constant, "stochastic": False},
    "gaussian_white_noise": {"func": generate_gaussian_white_noise, "stochastic": True},
    "uniform_noise": {"func": generate_uniform_noise, "stochastic": True},
    "pink_noise": {"func": generate_pink_noise, "stochastic": True},
    "sine": {"func": generate_sine, "stochastic": False},
    "sine_trend": {"func": generate_sine_trend, "stochastic": False},
    "ar1": {"func": generate_ar1, "stochastic": True},
    "lorenz": {"func": generate_lorenz, "stochastic": True}, # Sensitive to initial conditions
    "changepoint": {"func": generate_changepoint, "stochastic": True}
}

def calculate_mean_M(m_dict):
    # Simple heuristic to extract a scalar from Memory profile if it's a dict or list
    if isinstance(m_dict, dict):
        vals = list(m_dict.values())
        return np.mean(vals) if len(vals) > 0 else np.nan
    elif isinstance(m_dict, (list, np.ndarray)):
        return np.mean(m_dict) if len(m_dict) > 0 else np.nan
    return float(m_dict)

def execute_lab():
    summary_data = []
    
    for name, config in SIGNALS.items():
        print(f"Testing {name}...")
        func = config["func"]
        is_stochastic = config["stochastic"]
        runs = N_RUNS if is_stochastic else 1
        
        results_for_signal = []
        for i in tqdm(range(runs)):
            try:
                if is_stochastic:
                    sig = func(n=N_POINTS, seed=i)
                else:
                    sig = func(n=N_POINTS)
                # Reshape if necessary, ICCS expects 1D or 2D. We provide 1D.
                prof = run_iccs(sig)
                
                if "error" in prof:
                    res = {"run": i, "error": prof["error"], "M_mean": np.nan, "D_local": np.nan, "TE_fwd": np.nan}
                else:
                    m_mean = calculate_mean_M(prof["M"]) if prof["M"] is not None else np.nan
                    d_local = float(prof["D_local"]) if prof["D_local"] is not None else np.nan
                    te_fwd = float(prof["TE_forward"]) if prof["TE_forward"] is not None else np.nan
                    
                    res = {
                        "run": i, 
                        "M_mean": m_mean, 
                        "D_local": d_local, 
                        "TE_fwd": te_fwd,
                        "raw_profile": prof
                    }
                results_for_signal.append(res)
            except Exception as e:
                results_for_signal.append({"run": i, "error": str(e), "M_mean": np.nan, "D_local": np.nan, "TE_fwd": np.nan})
                
        # Save raw results
        raw_path = os.path.join(RAW_DIR, f"{name}_raw.json")
        with open(raw_path, 'w') as f:
            # We filter out non-serializable objects if any, but our proxy is dict of floats
            clean_results = []
            for r in results_for_signal:
                clean_r = {k: v for k, v in r.items() if k != "raw_profile"}
                clean_results.append(clean_r)
            json.dump(clean_results, f, indent=2)
            
        # Aggregate statistics
        df = pd.DataFrame(results_for_signal)
        
        if len(df) == 0:
            continue
            
        agg = {"Signal": name, "Runs": runs}
        
        for col in ["M_mean", "D_local", "TE_fwd"]:
            if col in df.columns:
                valid_data = df[col].dropna()
                agg[f"{col}_mean"] = valid_data.mean() if len(valid_data) > 0 else np.nan
                if runs > 1:
                    std = valid_data.std()
                    # 95% CI roughly 1.96 * std / sqrt(n)
                    ci = 1.96 * std / np.sqrt(len(valid_data)) if len(valid_data) > 0 else np.nan
                    agg[f"{col}_std"] = std
                    agg[f"{col}_ci95"] = ci
                    
        summary_data.append(agg)
        
        # Plotting distributions for stochastic
        if runs > 1:
            fig, axes = plt.subplots(1, 3, figsize=(15, 4))
            for idx, col in enumerate(["M_mean", "D_local", "TE_fwd"]):
                if col in df.columns:
                    axes[idx].hist(df[col].dropna(), bins=10, alpha=0.7)
                    axes[idx].set_title(col)
            plt.suptitle(f"{name} metrics distribution (N={runs})")
            plt.tight_layout()
            plt.savefig(os.path.join(FIGURES_DIR, f"{name}_dist.png"))
            plt.close()

    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(TABLES_DIR, "summary_metrics.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"\nFalsification lab complete. Summary saved to {summary_path}")

if __name__ == "__main__":
    execute_lab()
