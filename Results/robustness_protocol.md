# Robustness Evaluation Protocol (v0.1.1)

## Epistemological Stance
In alignment with the Boundary Validation Protocol (BVP), the goal of this robustness evaluation is not to definitively "prove" the validity of the ICCS feature space, nor to "find a flaw" to reject it. Rather, the goal is to **characterize the failure regime** of the estimators under empirical constraints. 

**Interpretation Principle:**
Failure of an estimator component does not invalidate the structural representation. It identifies the empirical operating domain of that component.

## Experimental Parameters

### General Setup
- **Framework Version**: `psf 0.1.0` (ICCS v1.1)
- **Randomness**: Strict reproducibility is enforced. All generators use `np.random.default_rng(seed)`.
- **Seed**: `42` (Fixed across all baseline calculations and explicitly logged in `robustness_raw.csv`).

### Data Generators
1. **Lorenz System**: Deterministic chaos. Subsampled `dt=0.01`, $X$ coordinate.
2. **AR(1)**: Stochastic process. $X_t = 0.9 X_{t-1} + \epsilon$.
3. **Causal System (X $\rightarrow$ Y)**: Bivariate coupled system with $Y_t = 0.5 Y_{t-1} + 0.8 X_{t-1} + \epsilon$.
4. **Predictive Mimic**: Uncoupled bivariate harmonic oscillators with matched predictive Mutual Information via noise tuning.

> [!NOTE]
> **Observational Noise:** Noise is applied *after* system generation and does not alter the generating dynamic mechanism. It serves strictly as observational corruption: $X_{noise} = X + \mathcal{N}(0, 1) \cdot \alpha \cdot \sigma(X)$.

## Evaluation Suite

### Experiment 1: Noise Robustness
- **Sample Size ($N$)**: Fixed at 5000.
- **k-neighbors**: Fixed at $k=10$.
- **Noise Levels ($\alpha$)**: `[0.0, 0.01, 0.05, 0.10, 0.20]` (0% to 20%).
- **Objective**: Track the component-wise absolute deviations ($\Delta M, \Delta D_{local}, \Delta TE, \Delta CMI$) and the normalized total vector shift ($\Delta S$) relative to the 0% noise baseline.

### Experiment 2: Sample Size Convergence
- **Noise Level**: Fixed at 0.0 (Clean).
- **k-neighbors**: Fixed at $k=10$.
- **Sample Sizes ($N$)**: `[250, 500, 1000, 5000, 10000]`.
- **Objective**: Identify the minimum data requirements for each structural feature to stabilize. 

### Experiment 3: Boundary Preservation
- **Metric**: Analyzed from Experiment 1's outputs.
- **Absolute Gap**: $TE_{causal} - TE_{mimic}$
- **Relative Gap**: $\frac{TE_{causal} - TE_{mimic}}{TE_{causal} + TE_{mimic} + \epsilon}$
- **Objective**: Determine if the BVP-defined structural separation between a truly causal system and a predictive mimic is maintained even when absolute metric values degrade.

## Pass/Fail Criteria (Validity Boundaries and Failure Regimes)
A feature space component enters its failure regime when:
1. Its convergence variance with respect to sample size $N$ fails to plateau.
2. Its noise degradation outpaces the baseline signal, causing identical underlying structures to yield radically divergent profiles ($\Delta S_{relative} > 1.0$).
3. **Representation Boundary Failure**: The absolute deviation $|D(X) - D(f(X))|$ exceeds acceptable tolerance under permitted transformations (e.g., rotation/scaling).
4. **Causal Boundary Failure**: 
   - The Relative Gap between Causal and Mimic drops below $0.1$.
   - OR, the absolute signal strength drops below the estimator's noise floor ($TE_{causal} < \epsilon$), making any relative gap mathematically valid but practically meaningless.
