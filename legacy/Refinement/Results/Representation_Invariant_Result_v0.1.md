# Representation-invariant Result v0.1

## Candidate

Rank-based Mutual Information

## Motivation

Boundary #2 showed that raw predictive information
depends on representation geometry.

Rank normalization was tested as a correction.

## Experiment

Transformations:

- scaling
- cubic bijection
- permutation
- rotation

Metric:

Memory profile:

$M = \sum I(rank(X_t);rank(X_{t+k}))$

## Results

| Transform | $\Delta M_{rank}$ | Result |
|---|---:|---|
| Scaling | 0.09% | PASS |
| Cubic | 0.03% | PASS |
| Permutation | 32.15% | FAIL |
| Rotation | 21.62% | FAIL |

## Boundary Found

Rank normalization removes dependence on marginal distributions,
but does not provide invariance under coordinate mixing.

## Conclusion

Rank-MI is accepted as a partial normalization method,
not as a representation-invariant dynamics descriptor.

## Implication for next candidate

The failure mode indicates that the remaining problem is not marginal distribution dependence, but geometric dependence caused by coordinate mixing.

Therefore, the next candidate should operate on intrinsic geometry of the state space rather than coordinate values.
