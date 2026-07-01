# Empirical Failure Regimes

This table summarizes the operational failure regimes of the ICCS feature space components under observational noise boundaries, establishing the boundaries of validity for each structural axis.

| Component   | Failure mode           | Observed threshold | Interpretation          |
| ----------- | ---------------------- | ------------------ | ----------------------- |
| $M(k)$      | predictive degradation | low noise levels   | gradual predictive attenuation; detectable degradation begins at low noise |
| $D_{local}$ | manifold distortion    | $> 20\%$ noise     | geometry collapse       |
| $TE$ (chaotic, weak coupling) | causal uncertainty | early collapse ($5\%$) | directional signal loss |
| $TE$ (strong causal coupling) | causal uncertainty | persistent separation ($> 20\%$) | directional signal preserved |
| Aggregation | feature compensation   | scalar projection  | structural collapse     |

## Observations
- **Geometry** ($D_{local}$) is remarkably robust, resisting manifold distortion up to the maximal tested boundaries.
- **Predictive Memory** ($M$) degrades predictably and smoothly.
- **Causality** ($TE$) collapses early ($5\%$) for chaotic systems lacking strong linear coupling, yet remains robust ($> 20\%$) when true coupled dynamics outweigh observational perturbations.
- **Aggregation** (scalar projections like $L_2$ norm or sums) empirically fails the structural separation boundary. Scalar projections allow non-causal components to compensate for the absence of causal information, reducing structural separability.
