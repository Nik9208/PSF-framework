## ICCS v1.0 Release

This release contains the full experimental implementation of the ICCS framework, including:

- regime extraction pipeline
- transition graph construction
- curvature-based instability metrics
- causal risk field estimation
- meta-optimization layer

### Key Contributions

- Koopman-consistent latent regime discovery
- falsification-tested against noise, shuffled, and chaotic systems
- baseline comparison against HMM, change-point detection, and spectral methods
- integrated control and meta-learning loop

### Evaluation

Validated across:

- Logistic map (order → chaos transition)
- Lorenz system
- Brownian motion
- shuffled surrogate datasets

### Baselines

- PCA + GMM
- UMAP + HDBSCAN
- HMM proxy
- Koopman spectral embedding proxy
- Change-point detection

### Result Summary

ICCS shows:
- strong alignment with Koopman-style representations
- clear separation from statistical segmentation methods
- robustness under falsification tests

### Status

Experimental research framework — not a production library.
