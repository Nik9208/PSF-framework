import os
import sys
import json
import subprocess
from datetime import datetime
import numpy as np
import pandas as pd

# Add ICCS core to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE3_DIR = os.path.dirname(BASE_DIR)
SRC_DIR = os.path.abspath(os.path.join(PHASE3_DIR, "..", "..", "..", "src"))
sys.path.append(SRC_DIR)

try:
    from psf.iccs import ICCS
except ImportError:
    print("ERROR: Could not import ICCS from src/psf/iccs.py")
    sys.exit(1)

REGISTRY_PATH = os.path.join(PHASE3_DIR, "registry", "dataset_registry.md")
PROC_DIR = os.path.join(BASE_DIR, "processed")
LEDGER_PATH = os.path.join(PHASE3_DIR, "registry", "Evidence_Ledger.md")

LAYERS = {
    "RAW": "econ_returns_raw.csv",
    "FT": "econ_returns_ft.csv",
    "IAAFT": "econ_returns_iaaft.csv"
}

def get_git_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT).decode('utf-8').strip()
    except Exception:
        return "N/A"

def update_ledger(evidence_id, text):
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(f"**{evidence_id}**\n{text}\n\n")

def run_layer_analysis(layer_name, file_name, save_csv=True, X_override=None):
    print(f"\n--- Analyzing Layer/Scenario: {layer_name} ---")
    
    if X_override is not None:
        X = X_override
    else:
        path = os.path.join(PROC_DIR, file_name)
        df = pd.read_csv(path)
        X = df['Log_Return'].values
    
    iccs = ICCS()
    profile = iccs.fit(X)
    
    # Result Validation
    for k, v in profile.vector.items():
        if np.isnan(np.array(v)).any() or np.isinf(np.array(v)).any():
            raise ValueError(f"Result Validation Failed for {layer_name}: NaN/Inf in {k}")
            
    print(f"PASS: ICCS execution and validation completed for {layer_name}.")
    
    # Save CSV
    if save_csv:
        results_df = pd.DataFrame({
            "Log_Return": X,
            "D_local": profile.vector["D_local"],
            "M": profile.vector["M"]
        })
        results_df["TE_forward"] = profile.vector["TE_forward"]
        results_df["TE_reverse"] = profile.vector["TE_reverse"]
        results_df["CMI"] = profile.vector["CMI"]
        
        csv_path = os.path.join(BASE_DIR, f"iccs_results_{layer_name.lower()}.csv")
        results_df.to_csv(csv_path, index=False)
    
    return profile, X

if __name__ == "__main__":
    profiles = {}
    X_data = {}
    
    # 1. Standard 3-Layer Execution
    for layer, filename in LAYERS.items():
        prof, X = run_layer_analysis(layer, filename)
        profiles[layer] = prof
        X_data[layer] = X
        update_ledger(f"E001_ECON_{layer}", f"ICCS executed successfully on frozen {layer} log-returns dataset.")
        
    # 2. Tail Sensitivity Check (3-sigma clipping on RAW)
    raw_X = X_data["RAW"]
    mean_X = np.mean(raw_X)
    std_X = np.std(raw_X)
    clipped_X = np.clip(raw_X, mean_X - 3*std_X, mean_X + 3*std_X)
    
    clipped_prof, _ = run_layer_analysis("RAW_CLIPPED", "", save_csv=False, X_override=clipped_X)
    update_ledger("E002_ECON_TAIL_CHECK", "Tail Sensitivity Check (3-sigma clipping) executed successfully.")
    
    # 3. Fingerprint Calculation
    raw_te_asym = profiles["RAW"].vector["TE_reverse"] - profiles["RAW"].vector["TE_forward"]
    ft_te_asym = profiles["FT"].vector["TE_reverse"] - profiles["FT"].vector["TE_forward"]
    iaaft_te_asym = profiles["IAAFT"].vector["TE_reverse"] - profiles["IAAFT"].vector["TE_forward"]
    clipped_te_asym = clipped_prof.vector["TE_reverse"] - clipped_prof.vector["TE_forward"]
    
    raw_M = np.mean(profiles["RAW"].vector["M"])
    ft_M = np.mean(profiles["FT"].vector["M"])
    iaaft_M = np.mean(profiles["IAAFT"].vector["M"])
    clipped_M = np.mean(clipped_prof.vector["M"])
    
    raw_D = np.mean(profiles["RAW"].vector["D_local"])
    ft_D = np.mean(profiles["FT"].vector["D_local"])
    iaaft_D = np.mean(profiles["IAAFT"].vector["D_local"])
    clipped_D = np.mean(clipped_prof.vector["D_local"])
    
    fingerprint = {
        "Geometry_Dlocal": {
            "RAW": raw_D,
            "FT": ft_D,
            "IAAFT": iaaft_D,
            "RAW_CLIPPED": clipped_D
        },
        "Memory_Depth": {
            "RAW": raw_M,
            "FT": ft_M,
            "IAAFT": iaaft_M,
            "RAW_CLIPPED": clipped_M
        },
        "TE_Asymmetry": {
            "RAW": raw_te_asym,
            "FT": ft_te_asym,
            "IAAFT": iaaft_te_asym,
            "RAW_CLIPPED": clipped_te_asym,
            "Delta_RAW_FT": raw_te_asym - ft_te_asym,
            "Delta_RAW_IAAFT": raw_te_asym - iaaft_te_asym,
            "Delta_RAW_CLIPPED": raw_te_asym - clipped_te_asym
        }
    }
    
    metadata = {
        "domain": "Economics (S&P 500 Daily Log-Returns)",
        "iccs_version": "0.3.1",
        "analysis_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "python_version": sys.version.split()[0],
        "git_commit": get_git_commit(),
        "protocol": "Phase3 v1.0",
        "surrogate_sensitivity_fingerprint": fingerprint
    }
    
    json_path = os.path.join(BASE_DIR, "analysis_metadata_econ.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        
    update_ledger("E003_ECON_FINGERPRINT", "Economics Surrogate and Tail Sensitivity Fingerprint generated.")
    
    print("\n--- Structural Fingerprint (Economics) ---")
    print(json.dumps(fingerprint, indent=4))
    print("\n[Phase 3.1C ICCS Execution Complete]")
