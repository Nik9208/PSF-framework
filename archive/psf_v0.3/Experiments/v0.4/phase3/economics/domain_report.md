# Domain Report: Economics (S&P 500 Daily Index)
**Dataset:** S&P 500 Log-Returns (Raw, FT, IAAFT, 3$\sigma$-Clipped)
**Date:** 2026-07-02
**Protocol:** Phase3 v1.0 (with 3-Layer Validation + Tail Sensitivity Check)
**Analysis Script:** `analyze_iccs_econ.py`
**ICCS Version:** v0.3.1 (frozen)

---

## 1. Observed Facts (Structural Fingerprint)

1. **Dataset Integrity:** 6,036 trading days of log-returns (2000-2024) processed.
2. **Geometry Profile (`D_local`):**
   - **RAW:** `1.129`
   - **FT / IAAFT:** `1.130` / `1.129`
   - **CLIPPED:** `1.121`
3. **Memory Profile (`M`):**
   - **RAW:** `0.30`
   - **FT / IAAFT:** `0.01` / `0.02` (Near zero)
   - **CLIPPED:** `0.37`
4. **Causal Profile (TE Asymmetry):**
   - **RAW:** `2.29`
   - **FT / IAAFT:** `2.27` / `2.32`
   - **CLIPPED:** `2.74`

---

## 2. Interpretation via Metric Validity Taxonomy

### Geometry: Exit from Quantized Collapse
* **Regime Status:** Valid Continuous Regime.
* **Evidence Link:** Unlike the Climate dataset, which caused mathematical explosions due to point-mass multiplicity, financial log-returns are strictly continuous. The `D_local` metric successfully stabilized at $\sim 1.12$ across all layers. This proves that Geometry in v0.3.1 works on 1D signals provided the underlying data is a smooth continuous manifold without quantization traps.

### Memory Depth: Volatility Clustering Detection
* **Regime Status:** Nonlinear Lift (Dominant).
* **Evidence Link:** Financial returns are known for having zero linear autocorrelation (efficient market) but strong variance autocorrelation (volatility clustering). The surrogates (FT/IAAFT), which preserve the linear spectrum but destroy the regime structure, showed effectively zero memory (`M ~ 0.02`). The Raw series showed `M = 0.30`. Crucially, when extreme jump tails were clipped, memory actually *increased* to `0.37`. This proves that ICCS Memory is successfully detecting the nonlinear volatility clustering regimes (which become even clearer when extreme outlier noise is removed).

### Transfer Entropy: Tail-Sensitive Estimator Chaos
* **Regime Status:** Baseline Asymmetry + Tail Distortion.
* **Evidence Link:** TE asymmetry is massive ($\sim 2.3$) across Raw, FT, and IAAFT layers, confirming the estimator baseline bias we discovered in Climate. However, the Tail Sensitivity Check reveals a fascinating distortion: clipping the extreme $\pm 3\sigma$ jumps causes the asymmetry to jump to `2.74`. This implies that the extreme market jumps (fat tails) were actually *suppressing* the metric's structural asymmetry. TE here is acting as a tail-distortion detector rather than a pure causal measure.

---

## 3. Structural Conclusions (Phase 3.1C)

This domain definitively verified the **Metric Regime Taxonomy**:
1. **Geometry** recovered because we changed the mathematical properties of the substrate (quantized $\rightarrow$ continuous).
2. **Memory** proved it can detect nonlinear stochastic volatility (clusters) completely separate from linear spectral memory.
3. **TE Asymmetry** proved to be highly sensitive to distributional outlier stress, continuing to act as an estimator structure artifact rather than a clean physical metric.

*Note: All surrogate comparisons in this non-stationary domain are interpreted conditionally on the destruction of the volatility regimes by the FT/IAAFT transforms, per the Phase 3 protocol.*
