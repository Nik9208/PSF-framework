import os
import sys
import hashlib
from datetime import datetime
import numpy as np
import pandas as pd
import urllib.request

# =============================================================================
# Paths Setup
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE3_DIR = os.path.dirname(BASE_DIR)
REGISTRY_DIR = os.path.join(PHASE3_DIR, "registry")
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROC_DIR = os.path.join(BASE_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# =============================================================================
# Step 1: Download and Parse NOAA Data
# =============================================================================
def download_nina34():
    url = "https://psl.noaa.gov/data/correlation/nina34.data"
    raw_txt_path = os.path.join(RAW_DIR, "nina34_raw.txt")
    print("Downloading NOAA Nino 3.4 SST data...")
    try:
        urllib.request.urlretrieve(url, raw_txt_path)
    except Exception as e:
        print(f"Failed to download data: {e}")
        sys.exit(1)
        
    # Parse the file
    # Format: 
    # Year1 Year2
    # YYYY M1 M2 M3 ... M12
    # Missing = -99.99
    
    with open(raw_txt_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    start_year, end_year = map(int, lines[0].strip().split())
    
    data = []
    # Data rows are from index 1 to (end_year - start_year + 1)
    # The last rows contain missing value specifier (-99.99) and blanks
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) == 13: # Year + 12 months
            year = int(parts[0])
            if start_year <= year <= end_year:
                values = [float(x) for x in parts[1:]]
                data.extend(values)
                
    data = np.array(data)
    valid_data = data[data != -99.99]
    
    raw_csv_path = os.path.join(RAW_DIR, "climate_raw.csv")
    pd.DataFrame({'SST': valid_data}).to_csv(raw_csv_path, index=False)
    
    raw_hash = get_sha256(raw_csv_path)
    print(f"Parsed {len(valid_data)} months of data. Saved to {raw_csv_path}")
    return valid_data, raw_csv_path, raw_hash

# =============================================================================
# Step 2: Surrogate Generation
# =============================================================================
def generate_ft_surrogate(X):
    X_f = np.fft.rfft(X)
    phases = np.random.uniform(0, 2 * np.pi, len(X_f))
    X_f_surr = np.abs(X_f) * np.exp(1j * phases)
    X_f_surr[0] = X_f[0] # preserve mean phase
    X_surr = np.fft.irfft(X_f_surr, n=len(X))
    X_surr = (X_surr - np.mean(X_surr)) / np.std(X_surr) * np.std(X) + np.mean(X)
    return X_surr

def generate_iaaft_surrogate(X, max_iter=1000):
    X_sorted = np.sort(X)
    X_f_orig = np.abs(np.fft.rfft(X))
    
    X_surr = np.random.permutation(X)
    
    for _ in range(max_iter):
        X_f = np.fft.rfft(X_surr)
        phases = np.angle(X_f)
        X_f_new = X_f_orig * np.exp(1j * phases)
        X_surr = np.fft.irfft(X_f_new, n=len(X))
        
        ranks = np.argsort(np.argsort(X_surr))
        X_surr_new = X_sorted[ranks]
        
        if np.allclose(X_surr, X_surr_new, atol=1e-6):
            break
        X_surr = X_surr_new
        
    return X_surr

# =============================================================================
# Step 3: Process and Log
# =============================================================================
def process_and_log(valid_data, raw_hash):
    np.random.seed(42)
    ft_surr = generate_ft_surrogate(valid_data)
    iaaft_surr = generate_iaaft_surrogate(valid_data)
    
    raw_proc_path = os.path.join(PROC_DIR, "climate_raw_processed.csv")
    ft_path = os.path.join(PROC_DIR, "climate_ft_surrogate.csv")
    iaaft_path = os.path.join(PROC_DIR, "climate_iaaft_surrogate.csv")
    
    pd.DataFrame({'SST': valid_data}).to_csv(raw_proc_path, index=False)
    pd.DataFrame({'SST': ft_surr}).to_csv(ft_path, index=False)
    pd.DataFrame({'SST': iaaft_surr}).to_csv(iaaft_path, index=False)
    
    raw_proc_hash = get_sha256(raw_proc_path)
    ft_hash = get_sha256(ft_path)
    iaaft_hash = get_sha256(iaaft_path)
    
    report = f"""# Preprocessing Log: Climate
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Steps Executed:
1. Parsed NOAA Niño 3.4 `.data` text matrix into 1D time series.
2. Filtered missing values (-99.99).
3. Generated FT Surrogate (Phase-randomized).
4. Generated IAAFT Surrogate (Iterative Amplitude Adjusted Fourier Transform).

## Summary:
- **Sample Length:** {len(valid_data)}
- **Raw CSV SHA256:** {raw_hash}
- **Processed Raw SHA256:** {raw_proc_hash}
- **FT Surrogate SHA256:** {ft_hash}
- **IAAFT Surrogate SHA256:** {iaaft_hash}

*Note: 3-Layer Validation Model Dataset Freeze In Effect.*
"""
    with open(os.path.join(BASE_DIR, "preprocessing_log.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print("Generated preprocessing_log.md")
    
    return raw_proc_hash, ft_hash, iaaft_hash, len(valid_data)

def generate_integrity_report(valid_data):
    n_total = len(valid_data)
    
    report = f"""# Data Integrity Report: Climate
**Dataset:** NOAA Niño 3.4 SST
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

| Criterion | Recorded | Value / Notes |
| :--- | :--- | :--- |
| Completeness | [x] | Total months: {n_total} |
| Missing value fraction | [x] | 0.0 (Filtered out -99.99 values) |
| Sampling frequency | [x] | 1 observation per month |
| Time span covered | [x] | {n_total / 12:.2f} years |
| Units of measurement| [x] | SST Anomaly (Celsius) |
| Effective sample length| [x] | {n_total} |
| Assumptions relevant to ICCS components| [x] | Presence of low-freq quasi-periodicity (ENSO cycle). |
"""
    with open(os.path.join(BASE_DIR, "integrity_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print("Generated integrity_report.md")

# =============================================================================
# Step 4: Update Registry
# =============================================================================
def update_registry(raw_hash, raw_proc_hash, ft_hash, iaaft_hash, observations):
    registry_path = os.path.join(REGISTRY_DIR, "dataset_registry.md")
    today = datetime.now().strftime('%Y-%m-%d')
    
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            if "NOAA Niño 3.4 SST" in line:
                # Add Raw
                parts = line.split('|')
                parts[1] = " **NOAA Niño 3.4 SST (Raw)** "
                parts[4] = f" {today} "
                parts[7] = f" {raw_hash} "
                parts[8] = f" {raw_proc_hash} "
                parts[9] = f" {observations} "
                parts[10] = " `climate_pipeline.py` v1 "
                raw_line = '|'.join(parts)
                
                # Add FT Surrogate
                parts[1] = " **NOAA Niño 3.4 SST (FT)** "
                parts[8] = f" {ft_hash} "
                ft_line = '|'.join(parts)
                
                # Add IAAFT Surrogate
                parts[1] = " **NOAA Niño 3.4 SST (IAAFT)** "
                parts[8] = f" {iaaft_hash} "
                iaaft_line = '|'.join(parts)
                
                new_lines.append(raw_line)
                new_lines.append(ft_line)
                new_lines.append(iaaft_line)
            else:
                new_lines.append(line)
                
        with open(registry_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print("Updated registry/dataset_registry.md with 3 layers.")

if __name__ == "__main__":
    valid_data, raw_csv_path, raw_hash = download_nina34()
    generate_integrity_report(valid_data)
    raw_proc_hash, ft_hash, iaaft_hash, obs = process_and_log(valid_data, raw_hash)
    update_registry(raw_hash, raw_proc_hash, ft_hash, iaaft_hash, obs)
    
    print("\n[Phase 3.1B Climate Data Processing Complete]")
    print("Next step: Run analyze_iccs_climate.py to generate 3-layer inference metrics.")
