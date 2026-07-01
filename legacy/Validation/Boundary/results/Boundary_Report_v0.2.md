# Boundary Validation Report v0.2

## Experiment

Adversarial Representations

## Objective

Test Observer Independence Principle under information-preserving transformations.

## Setup

A single dynamical system was observed through multiple bijective transformations:

- Original representation
- Linear scaling
- Rotation
- Cubic bijection
- Coordinate permutation

No transformation removed information.

## Results

| Observer | MI | ICCS |
|---|---:|---:|
| Original | 0.0568 | 0.0162 |
| Scaling | 0.0568 | 0.0162 |
| Rotation | 0.1563 | 0.1290 |
| Cubic | 0.0575 | 0.0184 |
| Permutation | 0.0385 | 0.0135 |

## Boundary Found

The current ICCS proxy is not invariant under all bijective transformations.

Two observers with equivalent information content may produce different structural estimates.

## Interpretation

This does not falsify PSF.

It identifies a limitation:

Current ICCS implementation mixes:

- system structure
- representation geometry
- estimator bias

## Required refinement

Future ICCS versions should separate:

1. representation-dependent measurements
2. invariant structural properties

Possible additions:

- transformation invariance testing
- observer equivalence classes
- geometry-normalized information metrics
