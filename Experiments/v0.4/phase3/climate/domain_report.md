# Domain Report: Climate (NOAA Niño 3.4 SST)
**Dataset:** NOAA Niño 3.4 SST (Raw, FT-Surrogate, IAAFT-Surrogate)
**Date:** 2026-07-02
**Protocol:** Phase3 v1.0 (with 3-Layer Validation Model)
**Analysis Script:** `analyze_iccs_climate.py`
**ICCS Version:** v0.3.1 (frozen)

---

## 1. Observed Facts (Surrogate Sensitivity Fingerprint)

1. **Dataset Integrity:** 917 months of continuous SST anomalies were successfully extracted (filtered out `-99.99` missing values).
2. **Infrastructure:** The 3-layer validation pipeline (Raw, FT, IAAFT) executed successfully.
3. **Geometry Profile (`D_local`):**
   - **RAW:** `13,812,839,642.67` (Catastrophic explosion)
   - **FT Surrogate:** `1.11` (Stable)
   - **IAAFT Surrogate:** `13,812,839,642.67` (Catastrophic explosion)
4. **Memory Profile (`M`):**
   - **RAW:** `2.20` steps
   - **FT Surrogate:** `1.80` steps
   - **IAAFT Surrogate:** `1.70` steps
5. **Causal Profile (TE Asymmetry = $TE_{rev} - TE_{fwd}$):**
   - **RAW:** `0.024`
   - **FT Surrogate:** `0.063`
   - **IAAFT Surrogate:** `0.062`

---

## 2. Interpretation Supported by Current Evidence

### Geometry: Metric Degeneracy Regime
* **Interpretation:** Undefined on discrete/quantized manifolds in 1D without embedding.
* **Evidence Link:** The `D_local` explosion is not an instability of empirical data; it is an effective metric collapse. Because NOAA SST is quantized (two decimals) and sampled over long stretches, it contains highly repeated identical values. In 1D without embedding, identical values yield zero distances, causing saturation and a logarithmic divergence explosion. The FT surrogate smooths the distribution (resolving the degeneracy to `D=1.11`), while IAAFT reintroduces the exact amplitude histogram (point-mass multiplicity), breaking the metric again. Geometry here does not measure dynamical structure; it measures the presence of point-mass multiplicity.

### Transfer Entropy: Baseline Directional Asymmetry
* **Interpretation:** Measurement-induced arrow of time.
* **Evidence Link:** TE asymmetry is actually stronger in the surrogates (~0.06) than in the raw data (~0.024). This is not merely an "error" but a structural null asymmetry floor—a property of the estimator's geometry within the finite-sample lagged embedding space. The real non-linear phase structure of ENSO (present only in RAW) does not create the asymmetry; rather, it *interferes* with the estimator's baseline asymmetry, reducing it. 

### Memory Depth: Spectral + Weak Nonlinear Persistence
* **Interpretation:** Stable anchor metric.
* **Evidence Link:** Memory is the only structurally stable component across all layers. It demonstrates a stable ordering: a baseline memory driven by the power spectrum (~1.7–1.8 in surrogates) and a small, consistent nonlinear lift (~0.4) contributed by the raw phase structure.

---

## 3. Remaining Uncertainties

1. **Geometry on Embedded Data:** Would delay embedding (currently omitted in v0.3.1) resolve the zero-distance saturation by separating identical values across temporal dimensions?
2. **TE Baseline Floor Origin:** What exact mathematical property of `compute_causal_fingerprint` induces the baseline directional asymmetry of ~0.06 on strictly phase-randomized stationary Gaussian noise?

---

## 4. Relation to Phase 3 Research Questions

| Research Question | Current Status |
| :--- | :--- |
| **RQ1 (Reproducibility)** | Metrics are reproducible, but Geometry is undefined under quantized regimes. |
| **RQ2 (Cross-domain regimes)** | Cannot be compared dynamically until estimator regimes are accounted for. |
| **RQ3 (Component stability)** | **Clean Decomposition:** Memory is stable. TE is structurally biased but consistent. Geometry is invalid under 1D quantization. |
| **RQ4 (Domain attribution)** | We successfully separated "physics" from "estimator failure modes." ICCS v0.3.1 acted not as a feature extractor, but as a regime detector of estimator behavior under data constraints. |
