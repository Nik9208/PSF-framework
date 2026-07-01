# Equal MI Different Dynamics

## Overview
This test evaluates whether the Information-based Consensus and Consistency Score (ICCS) can distinguish between systems that have identical predictive information (MI) but fundamentally different dynamical structures.

## Evaluated Systems
A. Lorenz chaotic attractor (Complex, high-dimensional chaos)
B. AR(1) stochastic persistence (Linear stochastic persistence)
C. Noisy periodic oscillator (Simple deterministic cycle with noise)
D. Deterministic low-dimensional system (e.g., Van der Pol)

## Hypothesis

**H0:**
Equal predictive information does not imply equal predictive structure.

**H1:**
Systems with equal MI can have different ICCS signatures.

## Failure condition

$ICCS(S_1) \approx ICCS(S_2)$

while:
- dynamical complexity differs
- attractor structure differs
- observer representations disagree

If the framework cannot distinguish these systems solely based on ICCS, it indicates that $MI$ (and stability) is insufficient, and $ICCS$ must be expanded (e.g., $ICCS = f(MI, Stability, Persistence)$).

## Result: Boundary Found (v0.3)

Two systems were constructed:

1. Lorenz chaotic attractor
2. AR(1) stochastic memory process

They exhibit different underlying dynamics:

- deterministic chaotic attractor vs stochastic process
- different distribution morphology
- different perturbation response

However, under the current ICCS proxy:

ICCS = f(MI, Stability)

the resulting scores converge:

Lorenz:
ICCS = 1.6844

AR(1):
ICCS = 1.6719

Difference:
$\Delta ICCS \approx 0.0125$

## Interpretation

The result indicates a limitation of the current ICCS proxy.

Predictive information and local stability alone are insufficient
to uniquely identify dynamical organization.

This does not falsify PSF itself.
It identifies a boundary condition requiring ICCS refinement.

## Required extension

Future ICCS versions may require additional structural terms:

- multi-step predictive geometry
- representation invariance
- attractor topology
- causal constraints
- observer agreement over transformations
