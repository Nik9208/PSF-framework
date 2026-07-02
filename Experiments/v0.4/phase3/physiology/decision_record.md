# Decision Record: Physiology (Pilot)
**Domain:** Physiology (NSRDB Subject 16265)
**Date:** 2026-07-02
**Context:** Phase 3.1A Execution Closure

## 1. Execution Status
* **Pipeline:** Completed
* **Dataset:** Frozen
* **ICCS run:** Successful (no execution errors)
* **Artifacts generated:** `integrity_report.md`, `preprocessing_log.md`, `iccs_results.csv`, `domain_report.md`

## 2. Data & Pipeline Integrity
* All protocol checks passed
* No missing values / NaN / Inf produced by the analysis
* Dataset registry updated and consistent
* SHA256 verified against frozen state

## 3. Key Observations (non-interpretive)
* `D_local` ≈ 0.00025
* `M` ≈ 9.06
* TE asymmetry observed (`TE_reverse` 4.31 > `TE_forward` 1.13)

## 4. Interpretation Status
All interpretations are documented in `domain_report.md` and remain conditional on implementation-specific properties of ICCS v0.3.1 and finite-sample estimators.

## 5. Open Questions carried forward
* Robustness of TE asymmetry across subjects and domains
* Sensitivity of Geometry to scalar projection limitation
* Influence of estimator properties vs. domain dynamics

## 6. Transition Statement
Phase 3.1A is considered complete at the level of pipeline execution and documentation.
Execution readiness is confirmed for the next domain.
Phase 3.1B (Climate domain) is initiated under identical protocol constraints and frozen methodology.
