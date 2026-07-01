# Observer Benchmark

## Testing Observer-Induced Representation Bias

---

# 1. Objective

The purpose of this benchmark is to test whether a machine learning model selects a representation because it is physically predictive or because of observer-specific bias.

The framework distinguishes:

Predictive structure

from

Observer-induced structure.

---

# 2. Principle

A model may assign high importance to a representation:

Importance_obs(Φ)

without that representation being the most predictive.

Therefore:

model importance ≠ predictive structure

---

# 3. Experimental Setup

The same dynamical system is analyzed using multiple observers:

- Linear Regression
- k-Nearest Neighbors
- Random Forest
- Neural Network
- Symbolic Regression

Each observer receives the same dynamical data.

---

# 4. Evaluation

For each representation:

measure:

## Predictive Accessibility

I(Φ,h)

and:

## Observer Preference

Importance_obs(Φ,h)

---

The framework compares:

physical predictive contribution

against:

model-selected importance.

---

# 5. Expected Cases

## Case A — Observer Agreement

Condition:

All observers select the same dominant representation.

Interpretation:

The representation is likely a robust predictive carrier.

---

## Case B — Observer Disagreement

Condition:

Different models select different representations.

Interpretation:

Possible observer-induced migration.

---

# 6. Van der Pol Example

System:

Van der Pol oscillator


Observed behavior:

Some models preferred a phase-based representation.

However, information analysis did not show a corresponding increase in predictive accessibility.

---

# 7. Framework Interpretation

The observed migration was classified as:

Observer-Induced Migration

not physical representation change.

---

# 8. ICCS Application

The Information Conditioned Carrier Score:

ICCS(Φ,h)

combines:

- predictive information;
- observer influence.

High ICCS:

observer agrees with predictive structure.

Low ICCS:

observer preference dominates.

---

# 9. Importance

This benchmark tests the central principle:

Machine learning models are measuring instruments.

They do not automatically reveal physical structure.

---

# Status

Validation component.

Framework concepts tested:

- Observer Independence Principle
- Observer-Induced Migration
- ICCS
