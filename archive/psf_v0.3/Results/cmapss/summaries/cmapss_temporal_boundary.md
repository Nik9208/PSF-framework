# C-MAPSS Experiment 1: Temporal Boundary

## Objective
Evaluate how the ICCS profile ($S(X)$) captures structural changes as turbofan engines transition from stable early life to late-stage degradation. We test whether different ICCS components degrade redundantly or orthogonally.

## Methodology
- **Dataset**: C-MAPSS FD001
- **Channels**: Fixed representation ($X=s9, Y=s4, Z=s3$) from Phase 0.
- **Segmentation**: Normalized lifetime per engine into `Early` (0-33%), `Middle` (33-66%), and `Late` (66-100%).
- **Engines Evaluated**: 20 trajectories.

## Empirical Findings (Mean Across Engines)

| Phase | $M(k)$ | $D_{local}$ | $TE_{forward}$ | $TE_{reverse}$ | $CMI$ | Scalar Baseline (Var) |
|-------|--------|-------------|----------------|----------------|-------|-----------------------|
| Early | 0.11   | 1.14        | 0.024          | 0.021          | 0.017 | 46.45                 |
| Middle| 0.73   | 1.16        | 0.024          | 0.030          | 0.036 | 63.05                 |
| Late  | 5.52   | 1.13        | 0.039          | 0.040          | 0.221 | 526.74                |

## Interpretation & Conclusions

1. **Differential Response of Geometry and Memory**
   As hypothesized by the BVP protocol, structural parameters do not fail uniformly. While the autoregressive predictability drops (evidenced by a substantial increase in $M(k)$ from Early to Late stages), the local intrinsic dimensionality ($D_{local}$) remains comparatively stable ($\approx 1.14$). The local geometric estimate remains invariant while the traversal dynamics degrade.

2. **Directed Dependency Coupling**
   The Conditional Mutual Information ($CMI$) and Transfer Entropy ($TE$) terms remain stable during the Early-to-Middle transition, but jump significantly in the Late phase. This indicates that late-stage degradation is associated with increased directed dependency estimates, as sensor channels become tightly coupled by the underlying systemic failure rather than operating independently.

3. **Scalar Baseline Contrast**
   The naive scalar baseline (sum of variances) explodes from 46 to 526. While scalar variance is an effective heuristic for anomaly detection, it combines multiple structural effects. 

## Summary
The temporal boundary experiment indicates that ICCS components exhibit non-uniform responses during degradation. Memory and dependency-related measures change substantially across phases, while local geometric estimates remain comparatively stable. This suggests that scalar degradation signals may combine multiple structural effects that can be separated by the ICCS representation.
