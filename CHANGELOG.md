# Changelog

All notable changes to this project will be documented in this file.

## [v0.3.1] - 2026-07-01
### Changed
- Refined manuscript terminology to strictly replace 'causal' claims with 'dependency' constructs, improving terminology consistency with the BVP evaluation framework.
- Integrated a unified Validation Framework structure into the manuscript, summarizing temporal, representation, noise, and baseline boundaries.
- Promoted `README_v0.2.md` to primary `README.md` and added standard project metadata (`CITATION.cff`, `CHANGELOG.md`).

## [v0.3.0] - 2026-07-01
### Added
- Baseline Discrimination Study on C-MAPSS FD001 (Experiment 4).
- Established empirical bounds separating ICCS behavior from scalar (Variance, Entropy) and low-dimensional (PCA) baselines.
- Structural Sensitivity Matrix to explicitly identify information not preserved by traditional metrics.

## [v0.2.1] - 2026-07-01
### Changed
- Restructured `Results/` directory (added `csv/`, `figures/`, `summaries/`) for structured reproducibility.
- Created `README_v0.2.md` as the primary reproducibility guide for the C-MAPSS validation suite.
- Replaced `seaborn` dependency with `matplotlib`.

## [v0.2.0] - 2026-07-01
### Added
- NASA C-MAPSS FD001 empirical validation suite.
- Unbiased channel selection protocol using variance filtering and Spearman complete-linkage clustering.
- Temporal boundary experiment demonstrating decoupled structural decay across engine lifespan.
- Representation boundary experiment evaluating information loss under smoothing and PCA compression.
- Noise boundary experiment confirming ICCS robustness under relative Gaussian observational noise.
