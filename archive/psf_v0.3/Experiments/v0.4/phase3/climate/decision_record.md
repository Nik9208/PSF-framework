# Decision Record: Climate (NOAA Niño 3.4 SST)
**Domain:** Climate (3-Layer Validation Model)
**Date:** 2026-07-02
**Context:** Phase 3.1B Execution Closure

## 1. Execution Status
* **Pipeline:** Completed (3-Layer Execution)
* **Dataset:** Frozen (Raw, FT-Surrogate, IAAFT-Surrogate)
* **ICCS run:** Successful (no execution errors, expected mathematical divergences correctly captured)
* **Artifacts generated:** `climate_pipeline.py`, `analyze_iccs_climate.py`, `preprocessing_log.md`, `integrity_report.md`, `domain_report.md`, `Metric_Regime_Taxonomy.md`

## 2. Data & Pipeline Integrity
* All protocol checks passed for all 3 layers.
* Dataset registry updated with dual-hash freezing for all 3 layers.

## 3. Key Observations (non-interpretive)
* `D_local` explodes to $\sim 10^{10}$ in RAW and IAAFT layers, but remains $\sim 1.11$ in FT layer.
* `M` depth displays stable hierarchy: RAW (2.20) > FT (1.80) > IAAFT (1.70).
* TE asymmetry exists in all layers, but is highest in FT (0.063) and lowest in RAW (0.024).

## 4. Interpretation Status
All component-level interpretations are officially delegated to the newly created **Metric Validity Taxonomy**. ICCS v0.3.1 Geometry is officially designated as *undefined* for 1D quantized un-embedded empirical data. TE asymmetry is formally designated as containing an intrinsic estimator baseline floor.

## 5. Open Questions carried forward
* Will Economics data (which is continuous and non-stationary) trigger the continuous geometry regime or reveal new failure modes?
* Does the estimator baseline asymmetry floor of TE vary with sample length $N$?

## 6. Transition Statement
Phase 3.1B is considered complete at the level of pipeline execution and structural validation.
The Surrogate Testing methodology has successfully isolated estimator structures from signal structures.
Execution readiness is confirmed for the next domain (Economics).
Phase 3.1C (Economics domain) is initiated under identical protocol constraints, but interpretations will now be strictly constrained by the `Metric_Regime_Taxonomy.md`.
