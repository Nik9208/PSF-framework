# PSF Framework v0.2 Reproducibility Guide

This guide provides the exact commands and environment requirements to reproduce the v0.2 empirical validation suite on the NASA C-MAPSS dataset.

## Environment Requirements

The following Python packages are required to run the validation scripts:
- `Python 3.8+`
- `numpy`
- `pandas`
- `scipy`
- `scikit-learn`
- `pyyaml`
- `matplotlib` (for generating figures)
- `seaborn` (for generating figures)

Ensure the `psf` package is installed in editable mode:
```bash
pip install -e .
```

## Execution Protocol

The validation suite is divided into four sequential scripts. They must be executed from the root of the repository.

### Phase 0: Channel Selection
Generates the unbiased baseline representation by removing near-constant sensors and reducing redundancy.
```bash
python Experiments/cmapss/00_channel_selection.py
```
*Outputs:* `Experiments/cmapss/selected_channels.yaml`

### Experiment 1: Temporal Boundary
Evaluates how ICCS components evolve across distinct degradation phases (Early, Middle, Late).
```bash
python Experiments/cmapss/01_iccs_cmapss_analysis.py
```
*Outputs:* `Results/cmapss/csv/cmapss_temporal_iccs.csv`

### Experiment 2: Representation Boundary
Tests the sensitivity of the ICCS representation to mathematical compression (PCA, Rolling means).
```bash
python Experiments/cmapss/02_iccs_representation_analysis.py
```
*Outputs:* `Results/cmapss/csv/cmapss_representation_iccs.csv`

### Experiment 3: Noise Boundary
Evaluates the robustness of structural signatures under 0-20% relative Gaussian observational noise.
```bash
python Experiments/cmapss/03_iccs_noise_analysis.py
```
*Outputs:* `Results/cmapss/csv/cmapss_noise_iccs.csv`

### Figure Generation
Generates the scientific visualizations used in the summaries.
```bash
python Experiments/cmapss/generate_figures.py
```
*Outputs:* PNG files in `Results/cmapss/figures/`
