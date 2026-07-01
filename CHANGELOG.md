# Changelog

All notable changes to the Boundary Validation Protocol (BVP) and the ICCS framework will be documented in this file.

## [0.1.0] - 2026-07-01

### Added
- **Boundary Validation Protocol (BVP)**: Formalized the iterative epistemology and algorithmic pipeline for structural metric validation.
- **ICCS v1.1 Feature Space**: Implemented the Information-theoretic Causal Complexity Score, consisting of Predictive Memory $M(k)$, Local Intrinsic Dimension $D_{local}$, and Causal Fingerprinting ($TE_{+}$, $TE_{-}$, $CMI$).
- **Boundary Benchmarks**: Defined and implemented four distinct structural ambiguity classes: Temporal, Representation, Causal, and Aggregation collapse.
- **Scientific Validation Tests**: Configured `test_boundary_validation.py` to assert relational boundaries natively in Python.
- **Initial Experiments Pipeline**: Included scripts for running the robustness and baseline tests over the benchmarks.
- **Core API (`psf`)**: Added an installable Python package exporting `from psf import ICCS` to enable frictionless computation of $S(X)$ profiles.
