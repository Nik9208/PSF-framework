# Representation test v0.2: Local Intrinsic Dimension

## Candidate
Local Intrinsic Dimension ($D_{local}$)

## Motivation
Rank-based MI successfully removed dependence on marginal distributions (scaling, cubic) but failed under coordinate mixing (rotation, permutation).
We hypothesize that intrinsic geometric properties (like local dimension) might offer invariance against coordinate mixing, as they operate in the intrinsic geometry of the state space rather than relying on axis-aligned marginals.

## Experiment
Systems: Base 2D nonlinear oscillator.
Transforms:
- Scaling
- Cubic bijection
- Permutation
- Rotation

Measure:
Maximum Likelihood Estimator of Intrinsic Dimensionality (Levina-Bickel estimator) based on k-Nearest Neighbors.

Compare:
$\Delta D = \frac{|D(T(X)) - D(X)|}{D(X)}$

## Criterion
Pass:
$\Delta D < \varepsilon$
where $\varepsilon$ is determined by identity numerical noise.
