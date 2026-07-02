import os
import sys
import json
import hashlib
from datetime import datetime
import numpy as np
import pandas as pd

# Paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Phase3/dummy/
PHASE3_DIR = os.path.dirname(BASE_DIR)
REGISTRY_DIR = os.path.join(PHASE3_DIR, "registry")
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROC_DIR = os.path.join(BASE_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def generate_synthetic_data():
    print("Generating synthetic infrastructure validation dataset...")
    
    # 1000 points of white noise
    np.random.seed(42)
    noise = np.random.normal(0, 1, 1000)
    
    raw_path = os.path.join(RAW_DIR, "dummy_raw.csv")
    df = pd.DataFrame({'Value': noise})
    df.to_csv(raw_path, index=False)
    
    raw_hash = get_sha256(raw_path)
    return noise, raw_path, raw_hash

def preprocess_and_log(data, raw_hash):
    steps = [
        "Loaded synthetic dummy data.",
        "Applied dummy filter (Values > -3 and < 3)."
    ]
    
    valid_data = data[(data > -3) & (data < 3)]
    steps.append(f"Removed {len(data) - len(valid_data)} outliers.")
    
    proc_path = os.path.join(PROC_DIR, "dummy_processed.csv")
    pd.DataFrame({'Value': valid_data}).to_csv(proc_path, index=False)
    proc_hash = get_sha256(proc_path)
    
    report = f"""# Preprocessing Log: Dummy Validation
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Steps Executed:
"""
    for i, step in enumerate(steps, 1):
        report += f"{i}. {step}\n"
        
    report += f"""
## Summary:
- **Original Sample Length:** {len(data)}
- **Effective Sample Length:** {len(valid_data)}
- **Data Retained:** {len(valid_data)/len(data)*100:.2f}%
- **Raw SHA256:** {raw_hash}
- **Processed SHA256:** {proc_hash}

*Note: Infrastructure Validation successful.*
"""
    with open(os.path.join(BASE_DIR, "preprocessing_log.md"), "w") as f:
        f.write(report)
    print("Generated preprocessing_log.md")
    return valid_data, proc_hash

def generate_integrity_report(raw_data):
    n_total = len(raw_data)
    n_missing = np.isnan(raw_data).sum()
    
    report = f"""# Data Integrity Report: Dummy Validation
**Dataset:** Synthetic White Noise
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

| Criterion | Recorded | Value / Notes |
| :--- | :--- | :--- |
| Completeness | [x] | Total points: {n_total} |
| Missing value fraction | [x] | {n_missing/n_total:.4f} ({n_missing} missing) |
| Sampling frequency | [x] | N/A (Arbitrary units) |
| Time span covered | [x] | N/A |
| Units of measurement| [x] | Arbitrary |
| Assumptions relevant to the applied ICCS components| [x] | i.i.d. strict stationarity |
| Effective sample length| [x] | {n_total - n_missing} |
"""
    with open(os.path.join(BASE_DIR, "integrity_report.md"), "w") as f:
        f.write(report)
    print("Generated integrity_report.md")

if __name__ == "__main__":
    print("=== Phase 3.0A: Infrastructure Validation ===")
    raw_data, path, raw_hash = generate_synthetic_data()
    generate_integrity_report(raw_data)
    proc_data, proc_hash = preprocess_and_log(raw_data, raw_hash)
    
    print("\n[Phase 3.0A completed — infrastructure validated.]")
    print("Files created in dummy/ directory. ICCS will NOT be launched.")
