# 📘 Phase 3 Regime Atlas
**ICCS v0.3.1 — Cross-Domain Measurement Regime Classification**

---

## 0. Core Statement

Phase 3 demonstrates that ICCS v0.3.1 does not operate as a universal feature extractor.

Instead, each component behaves as a **regime-dependent estimator**, whose output reflects a mixture of:
* properties of the underlying system
* properties of the data representation
* properties of the estimator itself
* finite-sample and numerical constraints

---

## 0.1 Epistemic Status (Critical Context)

> This document does not describe properties of physical systems.
> It describes the observed behavior of statistical estimators under structured data regimes.

**Three layers of claims:**
* **Empirical layer:** observed metric outputs under frozen ICCS v0.3.1
* **Estimator layer:** behavior of measurement functions under controlled data regimes
* **Interpretive layer:** classification of failure modes across domains

> Only the empirical layer is invariant.
> All higher-level statements are regime-dependent interpretations.

---

## 1. Geometry Regime Atlas

### 1.1 Definition
Geometry in ICCS v0.3.1 is a **local intrinsic dimension estimator on scalar projections**, sensitive to:
* metric degeneracy
* sampling density
* distribution discretization
* absence of embedding structure

### 1.2 Regimes Observed

#### 🟢 Continuous Nonstationary Regime (Economics)
* **Example:** S&P 500 log-returns
* **Behavior:** stable finite geometry (~1.1)
* **Interpretation:**
  * estimator operates in valid metric space
  * no collapse or explosion

#### 🔴 Quantized Degeneracy Regime (Climate)
* **Example:** Niño 3.4 SST (discretized values)
* **Behavior:** divergence / explosion
* **Mechanism:**
  * repeated values $\rightarrow$ zero-distance collapse
  * log-density instability
* **Interpretation:**
  * geometry becomes undefined, not noisy

#### 🔴 Scalar Projection Collapse Regime (Physiology)
* **Example:** RR intervals (1D projection of nonlinear attractor)
* **Behavior:** near-zero dimension
* **Mechanism:**
  * projection destroys manifold structure
* **Interpretation:**
  * estimator measures representation loss, not system complexity

### 1.3 Geometry Invariant Failure Law
> Geometry is not a property of the system.
> It is a property of the **representation manifold under a metric estimator**.

---

## 2. Memory Regime Atlas

### 2.1 Definition
Memory (Hurst-like behavior in ICCS) measures:
> persistence of temporal correlation structure under scalar observation

### 2.2 Regimes Observed

#### 🟢 Autocorrelation Regime (Physiology)
* stable short-range memory (~9 steps)
* physiological regulation dynamics

#### 🟡 Spectral Persistence Regime (Climate)
* moderate memory (~2 steps)
* dominated by low-frequency structure
* surrogate-sensitive reduction

#### 🟢 Volatility Clustering Regime (Economics)
* elevated memory (~0.3–0.4 normalized scale)
* persists under FT/IAAFT degradation
* sensitive to regime segmentation, not raw values

### 2.3 Memory Invariant Law
> Memory is the most stable ICCS component,
> but it conflates:
* autocorrelation
* volatility clustering
* spectral persistence

---

## 3. Transfer Entropy Regime Atlas

### 3.1 Definition
TE in ICCS v0.3.1 is a **lagged conditional dependence estimator over reconstructed causal coordinates**, sensitive to:
* embedding artifacts
* finite-sample bias
* surrogate structure
* tail events

### 3.2 Regimes Observed

#### 🟡 Baseline Asymmetry Regime (All Domains)
* persistent TE asymmetry floor (~0.02–0.06)
* present even in FT surrogates
* **Interpretation:** estimator-intrinsic directional bias

#### 🔴 Surrogate-Dominant Regime (Climate)
* TE increases under FT/IAAFT vs raw
* **Interpretation:**
  * phase structure suppresses estimator bias
  * surrogate reveals estimator floor

#### 🔴 Tail-Distortion Regime (Economics)
* TE increases under clipping
* **Interpretation:**
  * extreme events mask baseline structure
  * heavy tails interfere with conditional estimation

#### 🟡 Embedding-Dependent Regime (Physiology)
* TE sensitive to internal reconstruction
* **Interpretation:** causal fingerprint depends on internal lag mapping

### 3.3 TE Invariant Failure Law
> TE is not a measure of causality.
> It is a measure of **conditional estimation stability under finite sampling and representation choice**.

---

## 4. Cross-Domain Invariant Failure Principles

### 4.1 Principle of Representation Dominance
All ICCS components are dominated by:
> data representation > system dynamics

### 4.2 Principle of Estimator Self-Structure
Every ICCS metric contains:
* intrinsic bias floor
* surrogate sensitivity profile
* regime-dependent collapse modes

### 4.3 Principle of Non-Universality
There exists no single regime where Geometry, Memory, and TE simultaneously reflect only system properties.

### 4.4 Principle of Measurement Reflexivity
> ICCS measures both the system and the failure modes of measuring the system.

---

## 5. Unified Cross-Domain Classification

| Domain     | Geometry             | Memory                | TE                  |
| ---------- | -------------------- | --------------------- | ------------------- |
| Physiology | projection collapse  | stable autocorr       | embedding-sensitive |
| Climate    | quantized degeneracy | spectral              | surrogate-dominant  |
| Economics  | continuous stable    | volatility clustering | tail-distorted      |

---

## 6. Final Theoretical Statement

ICCS v0.3.1 is best understood not as:
> a feature extraction system

but as:
> a **regime diagnostic system for statistical estimator validity under structured data constraints**

---

## 7. Implication for Phase 4

Phase 3 concludes that:
> improvement of ICCS requires not tuning parameters,
> but redesigning the measurement foundations of Geometry and TE.
