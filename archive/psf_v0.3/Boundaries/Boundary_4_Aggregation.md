# Boundary Test #4: Feature Collapse Boundary

## Objective

Test whether aggregation from the ICCS v1.1 feature space destroys structural distinctions.

Feature space:

$S(X) = [M, D_{local}, TE_{+}, TE_{-}, CMI]$

## Hypothesis

Naive scalar aggregation may collapse different structural organizations into identical scores.

A candidate aggregation should preserve separation between structurally distinct systems within the validated benchmark suite.
$S(A) \not\sim S(B) \implies ICCS(A) \not\approx ICCS(B)$

## Systems

### System A — Predictive Mimic
High:
* M(k)

Low:
* TE asymmetry
* causal signal

Represents:
prediction without causation.

---

### System B — Direct Causal System
Moderate:
* M(k)

High:
* TE+
* causal asymmetry

Represents:
direct information transfer.

---

### System C — Complex Geometry System
High:
* D_local

Low:
* causal directionality

Represents:
complex state-space organization.

---

## Aggregations Tested

### 1. Linear
$I = w_1M + w_2D + w_3TE_{+} - w_4TE_{-} - w_5CMI$

Failure mode:
feature compensation.

---

### 2. Multiplicative
$I = M \cdot D^{-1} \cdot \max(0, TE_{+} - TE_{-}) \cdot e^{-CMI}$

Failure mode:
over-penalization.

---

### 3. Structural Distance
Aggregation is performed in feature space using distances or similarity measures rather than direct scalar projection.
$ICCS = f(d(S, S_{reference}))$

Preserves feature geometry.

---

### 4. Rank / Pareto aggregation
ICCS is not a scalar, but a partially ordered vector:
$ICCS = (M, D_{local}, TE_{+}, TE_{-}, CMI)$

## Acceptance Criterion

Aggregation passes if:
1. Predictive-only systems do not rank as causally equivalent.
2. Causal systems remain separated from mimics.
3. Geometric complexity is not confused with causal structure.
4. Small perturbations of S should not produce disproportionate changes in ICCS.

## Expected Outcome

The primary output of ICCS v1.1 is the structural feature vector ($S(X)$). Any scalar ICCS score is considered a derived summary and must not replace the underlying representation.
