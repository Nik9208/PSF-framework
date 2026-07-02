import os
import sys
import json
import hashlib
from datetime import datetime
import numpy as np
import pandas as pd
import subprocess

# Add ICCS core to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE3_DIR = os.path.dirname(BASE_DIR)
SRC_DIR = os.path.abspath(os.path.join(PHASE3_DIR, "..", "..", "..", "src"))
sys.path.append(SRC_DIR)

try:
    from psf.iccs import ICCS
except ImportError:
    print("ERROR: Could not import ICCS from PSF-framework/src/psf/iccs.py")
    sys.exit(1)

REGISTRY_PATH = os.path.join(PHASE3_DIR, "registry", "dataset_registry.md")
PROC_PATH = os.path.join(BASE_DIR, "processed", "processed_rr.csv")
LEDGER_PATH = os.path.join(PHASE3_DIR, "registry", "Evidence_Ledger.md")

def get_git_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT).decode('utf-8').strip()
    except Exception:
        return "N/A"

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def update_ledger(evidence_id, text):
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    if not os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "w") as f:
            f.write("# Evidence Ledger\n\n")
    
    with open(LEDGER_PATH, "a") as f:
        f.write(f"**{evidence_id}**\n{text}\n\n")

# =============================================================================
# Stage 1: Input Validation
# =============================================================================
def stage1_input_validation():
    print("--- Stage 1: Input Validation ---")
    if not os.path.exists(PROC_PATH):
        raise FileNotFoundError(f"Missing processed data: {PROC_PATH}")
        
    actual_hash = get_sha256(PROC_PATH)
    
    # Read registry
    expected_hash = None
    expected_obs = None
    script_version = None
    
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if "PhysioNet NSRDB" in line:
                parts = [p.strip() for p in line.split('|')]
                expected_hash = parts[8]
                expected_obs = int(parts[9])
                script_version = parts[10]
                break
                
    if actual_hash != expected_hash:
        raise ValueError(f"Dataset Freeze Violation! Hash mismatch.\nExpected: {expected_hash}\nActual: {actual_hash}")
        
    df = pd.read_csv(PROC_PATH)
    if len(df) != expected_obs:
        raise ValueError(f"Observation count mismatch. Expected: {expected_obs}, Actual: {len(df)}")
        
    print("PASS: Dataset Freeze and Analysis Freeze active. Hashes match.")
    update_ledger("E001_PHYS", "Dataset frozen and verified against registry.")
    update_ledger("E002_PHYS", "Integrity passed. Input validation successful.")
    return df, actual_hash, script_version

# =============================================================================
# Stage 2: ICCS Execution
# =============================================================================
def stage2_iccs_execution(df):
    print("--- Stage 2: ICCS Execution ---")
    X = df['RR_interval'].values
    
    # ICCS v0.3.1 run
    iccs = ICCS()
    profile = iccs.fit(X)
    
    print("PASS: ICCS execution completed.")
    update_ledger("E003_PHYS", "ICCS executed successfully on frozen dataset.")
    return profile

# =============================================================================
# Stage 3: Result Validation
# =============================================================================
def stage3_result_validation(profile):
    print("--- Stage 3: Result Validation ---")
    
    # Check for NaNs and Infs
    components = {
        "Geometry (D_local)": profile.vector["D_local"],
        "Memory (M)": profile.vector["M"],
        "Transfer (TE_fwd)": profile.vector["TE_forward"],
        "Transfer (TE_rev)": profile.vector["TE_reverse"],
        "Transfer (CMI)": profile.vector["CMI"]
    }
    
    validation_status = {}
    passed_all = True
    for name, val in components.items():
        val_np = np.array(val)
        is_nan = np.isnan(val_np).any()
        is_inf = np.isinf(val_np).any()
        
        if is_nan or is_inf:
            passed_all = False
            validation_status[name] = "FAIL (NaN/Inf detected)"
        else:
            validation_status[name] = "PASS"
            
    for name, status in validation_status.items():
        print(f"{name.split(' ')[0]:<10}: {status}")
        
    if not passed_all:
        raise ValueError("Result Validation Failed: ICCS produced NaNs or Infs.")
        
    print("PASS: All numerical checks passed.")
    update_ledger("E004_PHYS", "Result validation passed. No NaNs or Infs detected.")

# =============================================================================
# Stage 4: Metadata & Saving
# =============================================================================
def stage4_save_results(profile, df, dataset_hash, script_version):
    print("--- Stage 4: Metadata & Saving ---")
    
    # Save CSV
    results_df = pd.DataFrame({
        "RR_interval": df["RR_interval"].values,
        "D_local": profile.vector["D_local"],
        "M": profile.vector["M"]
        # TE components are scalar for the whole series in some implementations, 
        # or vectors. If scalars, we broadcast them, else we just save the vectors.
    })
    
    # TE and CMI are usually scalar. Let's add them as columns or metadata
    te_fwd = profile.vector["TE_forward"]
    te_rev = profile.vector["TE_reverse"]
    cmi = profile.vector["CMI"]
    
    results_df["TE_forward"] = te_fwd
    results_df["TE_reverse"] = te_rev
    results_df["CMI"] = cmi
    
    csv_path = os.path.join(BASE_DIR, "iccs_results.csv")
    results_df.to_csv(csv_path, index=False)
    
    # Save Metadata JSON
    metadata = {
        "dataset": "PhysioNet NSRDB (Subject 16265)",
        "dataset_sha256": dataset_hash,
        "iccs_version": "0.3.1",
        "analysis_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "python_version": sys.version.split()[0],
        "git_commit": get_git_commit(),
        "processing_script_version": script_version,
        "protocol": "Phase3 v1.0",
        "global_metrics": {
            "mean_D_local": np.mean(profile.vector["D_local"]),
            "mean_M": np.mean(profile.vector["M"]),
            "TE_forward": te_fwd,
            "TE_reverse": te_rev,
            "CMI": cmi
        }
    }
    
    json_path = os.path.join(BASE_DIR, "analysis_metadata.json")
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Results saved to {csv_path}")
    print(f"Metadata saved to {json_path}")
    print("\n[Phase 3.1A Data Processing Complete]")
    print("Next step: Produce domain_report.md based on iccs_results.csv")

if __name__ == "__main__":
    df, dataset_hash, script_version = stage1_input_validation()
    profile = stage2_iccs_execution(df)
    stage3_result_validation(profile)
    stage4_save_results(profile, df, dataset_hash, script_version)
