# Empirical Failure Regimes

This table summarizes the operational failure regimes of the ICCS feature space components under observational noise boundaries, establishing the boundaries of validity for each structural axis.

| Component   | Failure mode           | Observed threshold | Interpretation          |
| ----------- | ---------------------- | ------------------ | ----------------------- |
| $M(k)$      | predictive degradation | $> 0\%$ noise      | memory loss             |
| $D_{local}$ | manifold distortion    | $> 20\%$ noise     | geometry collapse       |
| $TE$        | causal uncertainty     | $5\% - 20\%$ noise | directional signal loss |
| Aggregation | feature compensation   | scalar projection  | structural collapse     |

## Observations
- **Geometry** ($D_{local}$) is remarkably robust, resisting manifold distortion up to the maximal tested boundaries.
- **Predictive Memory** ($M$) degrades predictably and smoothly.
- **Causality** ($TE$) collapses early ($5\%$) for chaotic systems lacking strong linear coupling, yet remains robust ($> 20\%$) when true coupled dynamics outweigh observational perturbations.
- **Aggregation** (scalar projections like $L_2$ norm or sums) empirically fails the structural separation boundary. Scalar metrics allow vast non-causal components to falsely compensate for an absence of causal flow.
