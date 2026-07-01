# Paper Outline

## Title

Predictive Structure Framework for Dynamical Systems: An Information-Based Approach to Predictive Representation Selection

---

# Abstract

## Goal

Describe a framework for identifying predictive structures in dynamical systems.

## Main idea

Predictive structure is not treated as a fixed object.

Instead:

The optimal representation depends on prediction horizon and accessible information.

## Main principle

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

---

# 1. Introduction

## Problem

Complex dynamical systems can often be represented in multiple ways.

Different representations may become useful at different prediction horizons.

Question:

How can we determine which representation carries predictive structure?

---

## Motivation

Machine learning models can discover useful representations.

However, model-selected features may reflect:

- architecture;
- optimization;
- inductive bias.

Therefore an observer-independent criterion is required.

---

# 2. Theoretical Framework

## 2.1 Predictive Representation

Define:

$$ \Phi $$

as a candidate representation of a dynamical system.

Predictive accessibility:

$$ I(\Phi,h) $$

measures information available for future prediction.

---

## 2.2 Optimal Representation

The optimal predictive representation:

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

---

# 3. Representation Regimes

## Regime I

Representation Migration

$$ \Phi_A \to \Phi_B $$

The dominant predictive carrier changes.

---

## Regime II

Representation Refinement

Same domain.

Improved mathematical description.

---

## Regime III

Information Horizon Collapse

Predictive information becomes inaccessible.

---

# 4. Observer Independence Principle

## Problem

A model may select a representation because it is convenient.

Not because it is physically predictive.

---

## Solution

Separate:

Predictive accessibility

from

Observer preference.

---

# 5. ICCS Metric

Information Conditioned Carrier Score:

$$ ICCS(\Phi,h) $$

Combines:

- predictive information share;
- observer influence.

---

# 6. Experiments

## Lorenz System

Purpose:

Test representation migration.

Result:

Local → cross-variable predictive transition.

---

## Rössler System

Purpose:

Test coordinate → phase representation change.

---

## Logistic Map

Purpose:

Test representation refinement.

---

## Van der Pol Oscillator

Purpose:

Test observer-induced migration.

---

## Duffing Oscillator

Purpose:

Test information collapse under uncertainty.

---

# 7. Limitations

The framework does not claim:

- predictive information equals causality;
- representation equals mechanism;
- ML discovers fundamental laws.

---

# 8. Future Work

Boundary Stress Tests:

- hidden variables;
- causal/predictive divergence;
- adversarial representations;
- equal information cases.

---

# Conclusion

The framework provides an operational method for analyzing how predictive structure appears, changes, and disappears in dynamical systems.
