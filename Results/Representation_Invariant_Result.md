# Representation-invariant Result v0.2

## Candidate

Local Intrinsic Dimension

## Motivation

Rank-based MI reduced marginal dependence but failed under coordinate mixing.

A geometry-based descriptor was tested as an alternative.

## Experiment

Transformations:

- scaling
- rotation
- permutation
- nonlinear bijection
- numerical noise

Metric:

MLE local intrinsic dimension estimator.

## Results

| Observer | D_local | $\Delta D$ |
|---|---:|---:|
| Original | 2.1895 | 0 |
| Noise | 2.1895 | 0 |
| Scaling | 2.1941 | 0.21% |
| Rotation | 2.1895 | 0 |
| Cubic | 2.1908 | 0.06% |
| Permutation | 2.1895 | 0 |

## Conclusion

Local intrinsic dimension passed the tested representation transformations.

It is accepted as:

Representation-invariant candidate v0.1.

Limitations:

- depends on sampling density
- depends on k-neighbor scale
- does not encode causality
