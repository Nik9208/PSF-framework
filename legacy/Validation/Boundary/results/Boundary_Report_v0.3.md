# Boundary Validation Report v0.3

## Experiment

Causal vs Predictive Divergence

## Objective

Test whether predictive structure is sufficient to identify causal structure.

Question:

Does:

Predictive Structure ≈ Causal Structure

hold under systems with different causal graphs?

---

## Systems Tested

### System A — Direct Causation

Structure:

X → Y

where future Y depends directly on previous X.

---

### System B — Common Driver

Structure:

      Z
     / \
    X   Y

where predictive dependence between X and Y
is produced by a hidden common source.

---

### System C — Reverse Predictive Direction

Structure:

Y → X

used to test whether predictive asymmetry
can identify direction.

---

## Results

| System | Forward MI | Reverse MI | CMI proxy | ICCS |
|---|---:|---:|---:|---:|
| Direct causal | 0.7345 | 0.3455 | N/A | 0.6838 |
| Common driver | 0.5945 | 0.5932 | 0.0000 | 0.5129 |
| Reverse | 0.4857 | 1.2816 | N/A | 0.4579 |

---

## Boundary Found

Predictive information alone does not uniquely determine causal organization.

The common-driver system produces predictive dependence between X and Y,
while conditional dependence disappears when controlling for the hidden variable Z.

---

## Interpretation

This does not falsify PSF.

It identifies a limitation:

Current predictive structure measures do not contain enough information
to infer causal structure without additional constraints.

---

## Required Refinement

Future ICCS versions may require:

- temporal directionality analysis
- conditional independence tests
- causal graph constraints
- intervention-based validation

---

## Summary of Boundary Series v0.1

Three independent limits identified:

1. Dynamics boundary:

Predictability + Stability ≠ Unique Structure

2. Observer boundary:

Information Preservation ≠ Representation Independence

3. Causality boundary:

Prediction ≠ Causation
