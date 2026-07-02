# Dynamics-aware Result v0.1

## Candidate

Multi-step Predictive Information

## Motivation

Boundary Validation v0.1 showed:

$I(X_t;X_{t+1}) + Stability$
was insufficient to distinguish different dynamical organizations.

## Experiment

Systems:

- Lorenz attractor
- AR(1) stochastic memory
- Periodic oscillator

matched on:

$I(X_t;X_{t+1})$

## Result

Memory profile:

$M = \sum I(X_t;X_{t+k})$

successfully separated systems.

Observed:

AR(1):
$M = 5.25$

Lorenz:
$M = 7.68$

Oscillator:
$M = 9.60$

## Conclusion

Multi-step predictive profile is accepted as a Dynamics-aware candidate.

It is not yet the final ICCS v1.1 component.
