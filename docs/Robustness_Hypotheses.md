# Robustness Evaluation Hypotheses

This document outlines the expected structural feature space behavior under empirical constraints, forming the basis for the *Validity Boundaries and Failure Regimes* evaluation. In accordance with the BVP, we establish these prior expectations so that divergences during the `v0.1.1` evaluation represent meaningful discoveries about the operational limits of the metrics.

## 1. Noise Degradation Expectations (Experiment 1)
- **Geometry ($D_{local}$)**: $D_{local}$ is expected to remain comparatively stable under moderate observational noise, provided that the local neighborhood structure is preserved.
- **Memory ($M$)**: $M(k)$ is expected to stabilize rapidly because it captures low-order temporal predictive structure before higher-order conditional dependencies become dominant.
- **Causality ($TE_{+}$, $CMI$)**: Expected to be the most sensitive to noise. Estimating conditional entropies in high-dimensional nearest-neighbor spaces relies on fine-grained neighborhood density. In kNN-based estimators this appears as increased neighborhood uncertainty rather than explicit density estimation error.

## 2. Sample Size Convergence Expectations (Experiment 2)
- **$M(k)$ Convergence**: Expected to stabilize rapidly ($N \approx 500$), as it captures low-order temporal predictive structure.
- **$D_{local}$ Convergence**: Expected to require moderate data to populate the local geometry manifold adequately ($N \approx 1000-5000$).
- **Causal Fingerprint Convergence**: Expected to require the most data ($N \ge 5000$) due to the curse of dimensionality inherent in estimating joint probability distributions for $X_{t}, X_{t-k}, Y_{t}, Y_{t-k}$ simultaneously. In kNN-based estimators this manifests as high neighborhood variance at low N.

## 3. Boundary Preservation Expectations (Experiment 3)
- We hypothesize that while absolute values of structural metrics (e.g., $TE_{causal}$ and $TE_{mimic}$) will plummet under heavy noise, the **Relative Gap** between them will remain robust up to a critical operational threshold (e.g., 10% relative noise).
- At the failure threshold, the relative gap will drop below 0.1, or the absolute causal signal will fall below the estimator's noise floor, marking the boundary where BVP Causal Separation fails.

## 4. Hyperparameter Stability (Experiment 4)
- **k-Nearest Neighbors ($k$)**: We expect the resulting structural separation to be robust to the choice of $k \in [5, 50]$. While absolute entropy bounds shift as neighborhood volumes change, the expected result is **qualitative stability of structural ordering** (Causal > Mimic) rather than identical numerical values.
