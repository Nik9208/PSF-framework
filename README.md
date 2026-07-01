# Predictive Structure Framework (PSF)

> An information-based framework for analyzing predictive representations in dynamical systems.

---

## Overview

PSF investigates how predictive structure appears, changes, and becomes inaccessible in dynamical systems.

---

## Scope

PSF is an operational framework.

It does not claim that predictive representations are identical to causal mechanisms or fundamental physical variables.

---

The central idea:

A dynamical system does not necessarily have a single fixed predictive representation.

The optimal representation depends on:

- prediction horizon,
- available information,
- representation space,
- observer constraints.

---

## Core Principle

The framework defines the optimal predictive representation:

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

where:

- $\Phi$ — candidate representation
- $h$ — prediction horizon
- $I(\Phi,h)$ — accessible predictive information

---

## Main Concepts

### Representation Migration

A change in the dominant predictive representation.

Example:

$$ \Phi_A \to \Phi_B $$

when another representation becomes more informative for prediction.

---

### Representation Refinement

The predictive domain remains the same, but the mathematical description improves.

---

### Information Horizon Collapse

At large horizons or high uncertainty, predictive information may become inaccessible.

---

### Observer Independence Principle

Machine learning models are treated as observers.

A model can select a representation because of:

- architecture,
- inductive bias,
- optimization preference.

Therefore:

**model importance $\neq$ physical predictive structure**

---

## Current Framework

Version:

Predictive Structure Framework v1.0-preprint

Status:

Research framework under validation.

---

## Repository Structure

```
Framework/
Core theory and mathematical definitions

Experiments/
Dynamical system validation

Validation/
Boundary and observer tests

Paper/
Publication drafts

Figures/
Future diagrams
```

---

## Systems Tested

- Lorenz
- Rössler
- Logistic Map
- Van der Pol
- Duffing oscillator

---

## Future Research

Boundary stress testing:

- hidden variables
- causal vs predictive divergence
- adversarial representations
- observer robustness

---

## License

Research project.
