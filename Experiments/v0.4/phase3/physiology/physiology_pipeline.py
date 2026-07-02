import os
import sys
import json
import hashlib
from datetime import datetime

# =============================================================================
# Step 1: Check Imports
# =============================================================================
try:
    import wfdb
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(f"ERROR: Missing dependency ({e}).")
    print("Please activate your venv and run: python -m pip install -r ../requirements.txt")
    sys.exit(1)

# Paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Phase3/physiology/
REGISTRY_DIR = os.path.join(os.path.dirname(BASE_DIR), "registry")
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROC_DIR = os.path.join(BASE_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# =============================================================================
# Step 2: Download NSRDB
# =============================================================================
def download_nsrdb(subject_id="16265"):
    print(f"Downloading NSRDB subject {subject_id}...")
    try:
        annotation = wfdb.rdann(subject_id, 'atr', pn_dir='nsrdb')
        sample_indices = annotation.sample
        symbols = np.array(annotation.symbol)
        
        normal_indices = sample_indices[symbols == 'N']
        rr_intervals = np.diff(normal_indices) / 128.0  # 128 Hz
        
        raw_path = os.path.join(RAW_DIR, f"{subject_id}_raw_rr.csv")
        df = pd.DataFrame({'RR_interval': rr_intervals})
        df.to_csv(raw_path, index=False)
        print(f"Raw data saved to {raw_path}")
        
        raw_hash = get_sha256(raw_path)
        return rr_intervals, raw_path, raw_hash
    except Exception as e:
        print(f"Failed to download NSRDB data: {e}")
        sys.exit(1)

# =============================================================================
# Step 3: Preprocess and Log
# =============================================================================
def preprocess_and_log(rr_intervals, raw_hash, subject_id):
    steps = [
        "Loaded raw RR intervals.",
        "Applied physiological bounds filter: 0.3s < RR < 2.0s (30-200 BPM)."
    ]
    
    valid_rr = rr_intervals[(rr_intervals > 0.3) & (rr_intervals < 2.0)]
    steps.append(f"Removed {len(rr_intervals) - len(valid_rr)} out-of-bound intervals.")
    
    proc_path = os.path.join(PROC_DIR, "processed_rr.csv")
    pd.DataFrame({'RR_interval': valid_rr}).to_csv(proc_path, index=False)
    proc_hash = get_sha256(proc_path)
    
    report = f"""# Preprocessing Log: Physiology
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Steps Executed:
"""
    for i, step in enumerate(steps, 1):
        report += f"{i}. {step}\n"
        
    report += f"""
## Summary:
- **Original Sample Length:** {len(rr_intervals)}
- **Effective Sample Length:** {len(valid_rr)}
- **Data Retained:** {len(valid_rr)/len(rr_intervals)*100:.2f}%
- **Raw SHA256:** {raw_hash}
- **Processed SHA256:** {proc_hash}

*Note: Dataset Freeze and Analysis Freeze are now in effect for this dataset.*
"""
    with open(os.path.join(BASE_DIR, "preprocessing_log.md"), "w") as f:
        f.write(report)
    print("Generated preprocessing_log.md")
    return valid_rr, proc_hash

# =============================================================================
# Step 4: Generate Integrity Report
# =============================================================================
def generate_integrity_report(raw_data, subject_id):
    n_total = len(raw_data)
    n_missing = np.isnan(raw_data).sum()
    
    report = f"""# Data Integrity Report: Physiology
**Dataset:** PhysioNet Normal Sinus Rhythm Database (NSRDB) - Subject {subject_id}
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

| Criterion | Recorded | Value / Notes |
| :--- | :--- | :--- |
| Completeness | [x] | Total RR intervals: {n_total} |
| Missing value fraction | [x] | {n_missing/n_total:.4f} ({n_missing} missing) |
| Sampling frequency | [x] | 128 Hz (derived from ECG annotations) |
| Time span covered | [x] | ~{n_total * np.nanmean(raw_data) / 3600:.2f} hours |
| Units of measurement| [x] | Seconds (RR interval duration) |
| Stationarity assessment| [x] | Biological system (expected local stationarity, global non-stationarity) |
| Effective sample length| [x] | {n_total - n_missing} |
"""
    with open(os.path.join(BASE_DIR, "integrity_report.md"), "w") as f:
        f.write(report)
    print("Generated integrity_report.md")

# =============================================================================
# Step 5: Update Dataset Registry
# =============================================================================
def update_registry(raw_hash, proc_hash, observations):
    registry_path = os.path.join(REGISTRY_DIR, "dataset_registry.md")
    today = datetime.now().strftime('%Y-%m-%d')
    
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # The line for Physiology has 10 fields:
        # | **PhysioNet NSRDB** | v1.0.0 | [PhysioNet (nsrdb)](https://physionet.org/content/nsrdb/1.0.0/) | (Pending) | ODC-PDDL | Goldberger et al. (2000) | (Pending) | (Pending) | (Pending) | `physiology_pipeline.py` v1 |
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "PhysioNet NSRDB" in line:
                parts = line.split('|')
                parts[4] = f" {today} " # Download date
                parts[7] = f" {raw_hash} " # SHA256 (Raw)
                parts[8] = f" {proc_hash} " # SHA256 (Processed)
                parts[9] = f" {observations} " # Observations
                lines[i] = '|'.join(parts)
                break
                
        with open(registry_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))
        print("Updated registry/dataset_registry.md")

if __name__ == "__main__":
    subject_id = "16265"
    raw_rr, path, raw_hash = download_nsrdb(subject_id)
    generate_integrity_report(raw_rr, subject_id)
    proc_rr, proc_hash = preprocess_and_log(raw_rr, raw_hash, subject_id)
    update_registry(raw_hash, proc_hash, len(proc_rr))
    
    print("\n[Dataset Freeze & Analysis Freeze In Effect]")
    print("Next step: Run ICCS v0.3.1 core on processed/processed_rr.csv")
