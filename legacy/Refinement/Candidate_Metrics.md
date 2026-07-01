# Candidate Metrics for ICCS v1.1

This document tracks potential mathematical components and estimators that satisfy the requirements defined in `ICCS_v1.1_Requirements.md`.

## 1. Dynamics-aware candidates

### Multi-step Predictive Information (Memory Profile)
**Metric:** $P(k)=I(X_t;X_{t+k})$ evaluated over multiple temporal lags $k=1,...,K$ with integrated memory estimate $M=\sum_{k=1}^{K}P(k)$

**Status:** Primary Dynamics candidate (passed dynamics validation)

**Purpose:** Measure temporal organization beyond one-step predictability. This addresses the limitation found in: Equal MI Different Dynamics Boundary.

**Hypothesis:** Systems with identical $I(X_t;X_{t+1})$ may have different long-range predictive profiles.

**Limitation:** Multi-step information does not necessarily capture causal structure or geometric organization.

---

### Recurrence-based Complexity
**Metric:** Recurrence Quantification Analysis (RQA) candidates: Recurrence Rate (RR) and Determinism (DET).

**Status:** Secondary exploratory candidate

**Purpose:** Measure temporal recurrence patterns that may not be visible through predictive information alone.

**Hypothesis:** Different dynamical organizations may produce different recurrence signatures even when short-term prediction is similar.

**Limitation:** RQA metrics depend on embedding dimension, delay parameter, distance metric, and recurrence threshold. Therefore they are treated as exploratory dynamics descriptors, not direct measures of structure.

---

## Evaluation protocol

A candidate dynamics metric is accepted only if it:
1. separates Lorenz and AR(1) under matched MI conditions;
2. does not collapse periodic deterministic systems with stochastic systems;
3. remains stable under parameter changes.

---

## Representation evaluation protocol

A candidate representation-invariant metric is accepted only if it:

1. preserves relative dynamics ordering under bijective transforms;
2. keeps $\Delta M$ below estimator noise level;
3. does not rely on coordinate orientation.

Primary stress cases:
- rotation
- nonlinear bijection
- permutation

---

## 2. Representation-invariant candidates

### Rank-based Mutual Information

**Status:** Representation-invariant candidate v0.1

**Method:**
Apply empirical rank transformation before MI estimation:
$X \rightarrow rank(X)/(N-1)$
then:
$P(k)=I(rank(X_t);rank(X_{t+k}))$

**Motivation:**
Reduce sensitivity of MI estimation to marginal distributions and coordinate scaling.

**Expected improvement:**
Lower representation variance under:
- scaling
- monotonic nonlinear transforms

**Known limitation:**
Rank transforms are not guaranteed invariant under arbitrary multivariate bijections. Rotation remains a critical test.

---

### Topological Dynamics Descriptors (TDA)

**Status:** Advanced candidate

**Purpose:** Capture candidate geometric invariants of the observed dynamics.

**Candidates:**
- Persistence diagrams
- Betti numbers

**Limitation:** Extreme computational complexity and high parameter sensitivity.

---

### Local Attractor Dimension

**Status:** Auxiliary candidate

**Purpose:** Estimate intrinsic dimensionality invariant to embedding scale.

---

## 3. Causal-aware candidates

### Causal Fingerprint

**Components:**
- directional information ($TE_{X \rightarrow Y}$)
- reverse direction control ($TE_{Y \rightarrow X}$)
- conditional dependence ($CMI$)

**Status:**
Causal candidate v0.1

**Purpose:**
Separate predictive association from causal organization. 

**Limitation:**
Requires conditional estimators and may depend on model assumptions. Residual approximation captures conditional dependence only under approximately linear assumptions.

---

## Causal-aware evaluation protocol

A causal candidate is accepted only if:
1. It distinguishes direct causal influence from common-driver correlation.
2. It preserves temporal directionality.
3. It does not collapse reverse causal systems into equivalent structures.

Stress tests:
- Direct causal chain: $X \rightarrow Y$
- Common driver: $Z \rightarrow X, Z \rightarrow Y$
- Reverse causal: $Y \rightarrow X$

Acceptance condition:
Predictive similarity must coexist with causal fingerprint separation.
