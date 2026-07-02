# ICCS v1.0: Experimental Validation Plan
**Objective:** Establish independent, robust empirical evidence for the structural claims made by the ICCS v1.0 architecture. Ensure a strict separation between implemented mechanisms and proposed theoretical properties.

## 1. Validation of Surrogate Diagnostics (Modules A-B)
**Claim:** The SCO, RSO, and TOO operators correctly distinguish structural signals from noise and temporal permutations.
**Required Experiments:**
- **False Positive Rate Analysis:** Apply operators to pure white noise and purely periodic signals. Verify that SCO scores remain near zero (within statistical error).
- **Alternative Explanations:** Compare SCO output against traditional permutation entropy and autocorrelation metrics to determine if ICCS captures unique structural information.

## 2. Validation of Phase Geometry & Clustering (Module C)
**Claim:** Latent embedding and clustering produce stable, separable representations of distinct dynamic regimes.
**Required Experiments:**
- **Robustness to Noise:** Inject varying levels of Gaussian and non-Gaussian noise into the synthetic benchmarks. Measure the degradation of the separation score ($S_{sep}$).
- **Alternative Methods:** Compare Spectral Embedding + KMeans against UMAP + HDBSCAN and standard PCA + GMM. Determine if the observed separation is an artifact of the specific clustering algorithm used.

## 3. Validation of Transition & Curvature (Modules D-E)
**Claim:** Markov transitions and local curvature proxies correctly identify bifurcation zones.
**Required Experiments:**
- **Ground Truth Comparison:** Test against a canonical dynamical system with known bifurcations (e.g., Logistic Map transitions into chaos, Lorenz attractor regime shifts). Check if "high curvature" points strictly align with known mathematical bifurcations.
- **Sensitivity Analysis:** Vary the temporal window size and sampling frequency. Assess how transition entropy ($H$) and deformation index respond to sampling resolution.

## 4. Validation of Causal Field & Control (Modules F-G)
**Claim:** The directed causal field predicts collapse regimes, and policy steering minimizes collapse energy.
**Required Experiments:**
- **Predictive Accuracy:** Use out-of-sample temporal sequences. Evaluate if states flagged as "high risk" reliably precede a structural collapse (measured by RSO drops).
- **Control Distortions:** Quantify the trade-off between stability gain and the required control shift ($||P - P'||$). Verify if the control policy merely creates a trivial self-loop rather than a structurally sound alternative regime.

## 5. Validation of Meta-Optimization (Module H)
**Claim:** Self-optimization over representation parameters identifies the most stable geometric embedding.
**Required Experiments:**
- **Overfitting Checks:** Perform cross-validation by optimizing on one segment of a time series and evaluating collapse energy on a held-out segment.
- **Degenerate Solutions:** Ensure the optimization does not trivially minimize collapse energy by setting $n\_clusters=1$ or mapping all states to a single point.

## Primary Benchmark Suite

### Deterministic Chaotic Systems
- Logistic Map
- Lorenz System
- Rössler Attractor

### Real-world time series
- S&P 500 returns
- FX exchange rates
- EEG / ECG datasets

### Null Models
- AR(1), ARIMA
- shuffled surrogate series
- phase-randomized signals

### Stress Tests
- Brownian motion
- Lévy flights

## Core Falsification Criteria
ICCS must survive three strict falsifications:
1. **Structural falsification**: "There are no regimes, but the system hallucinates them."
2. **Dynamical falsification**: "There are no transitions, but the system draws them."
3. **Causal falsification**: "There is no predictive power, only post-hoc interpretation."

## Open Questions & User Review Required

> [!WARNING]
> This document enforces strict separation between software implementation and scientific validity. The implemented system demonstrates computational feasibility, but the claims require empirical verification.
> 
> We are now ready to build the **ICCS v1.0 Evaluation Harness** to execute this exact validation plan against standard baselines (PCA+GMM, UMAP+HDBSCAN, HMM, Permutation Entropy).
