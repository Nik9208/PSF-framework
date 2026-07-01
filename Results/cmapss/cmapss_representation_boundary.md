# C-MAPSS Experiment 2: Representation Boundary

## Objective
Determine how different representation transformations (compression and smoothing) alter the structural dependency profile ($S(X)$) independently of the underlying degradation state. This experiment demonstrates that ICCS components are sensitive to specific representation losses, separating the effect of mathematical transformation from physical degradation.

## Methodology
- **Dataset**: C-MAPSS FD001 (First 20 engines).
- **Phases**: `Early` (0-33%) and `Late` (66-100%).
- **Representations**:
  1. **Raw (Dim=3)**: Unmodified $X, Y, Z$ channels.
  2. **Rolling (Dim=3)**: Moving average (window=10, center=False). Tests the effect of low-pass smoothing.
  3. **PCA-2 (Dim=2)**: First two principal components. Tests partial linear decorrelation.
  4. **PCA-1 (Dim=1)**: First principal component only. Tests absolute scalar collapse.

## Empirical Findings (Mean Across Engines)

| Phase | Representation | Dim | $M(k)$ | $D_{local}$ | $TE_{forward}$ | $TE_{reverse}$ | $CMI$ |
|-------|----------------|-----|--------|-------------|----------------|----------------|-------|
| Early | Raw            | 3   | 0.12   | 3.37        | 0.025          | 0.021          | 0.017 |
| Early | Rolling        | 3   | 2.29   | 2.84        | 0.023          | 0.043          | 0.181 |
| Early | PCA-2          | 2   | 0.10   | 2.40        | 0.014          | 0.029          | NaN   |
| Early | PCA-1          | 1   | 0.10   | 1.19        | NaN            | NaN            | NaN   |
|-------|----------------|-----|--------|-------------|----------------|----------------|-------|
| Late  | Raw            | 3   | 5.52   | 2.99        | 0.039          | 0.041          | 0.222 |
| Late  | Rolling        | 3   | 10.31  | 1.84        | 0.033          | 0.076          | 0.492 |
| Late  | PCA-2          | 2   | 6.87   | 2.15        | 0.025          | 0.031          | NaN   |
| Late  | PCA-1          | 1   | 6.87   | 1.14        | NaN            | NaN            | NaN   |

## Interpretation & Conclusions

1. **Dimensionality Tracking ($D_{local}$)**
   The local geometric estimate scales beautifully with the true degrees of freedom provided to the estimator: $\approx 3.0$ for Raw (3D), $\approx 2.2$ for PCA-2 (2D), and $\approx 1.1$ for PCA-1 (1D). Notably, `Rolling` smoothing artificially reduces the intrinsic dimensionality (from 3.37 to 2.84 in Early, and 2.99 to 1.84 in Late) by destroying high-frequency independent noise, collapsing the geometric manifold.

2. **The Smoothing Artifact Trap ($M(k)$ and $CMI$)**
   Applying a moving average (`Rolling`) severely corrupts the structural baseline. It artificially inflates autoregressive memory $M(k)$ in the healthy `Early` phase from 0.12 to 2.29. More critically, smoothing introduces massive artificial directed dependencies, inflating $CMI$ in the Early phase by 10x (0.017 to 0.181). This proves that common preprocessing techniques can fabricate structural signals that don't physically exist.

3. **PCA Destroys Dependency but Preserves Memory**
   `PCA-2` perfectly preserves the memory degradation profile (jumping from 0.10 to 6.87, identical to PCA-1), because memory is evaluated on the primary variance vector. However, linear orthogonalization heavily suppresses non-linear directed dependency: $TE_{forward}$ drops from 0.039 (Raw) to 0.025 (PCA-2) in the Late phase. PCA strips away the interacting structural components to minimize linear correlation, thereby erasing the directed causal signatures of systemic failure.

4. **One-dimensional Projection (PCA-1)**
   The PCA-1 representation tests the loss of multivariate structure under one-dimensional projection. The 1D projection preserves the scalar variance anomaly and the univariate memory increase ($M(k)$), but definitively forces the loss of all cross-channel dynamics ($TE$, $CMI$).

## Summary
Representation transformations are not neutral. Smoothing introduces artificial memory and dependencies, while PCA preserves memory but suppresses true directed interaction structures. The ICCS profile acts as an analytical boundary, isolating these mathematical artifacts from genuine physical state degradation.
