# Phase 2A: Geometry Representation Study (Pre-registered Protocol)

**Motivation:**
Following the findings of Phase 1, which identified operational limitations of the current Geometry representation when applied to scalar time series, Phase 2A evaluates whether Takens' delay embedding systematically alters the geometric representation and whether such changes are associated with improved discrimination between the benchmark systems evaluated in this study. Further work will be required to determine whether this improvement reflects more faithful reconstruction of the underlying dynamics or properties introduced by the embedding representation itself.

**Decision Rule for Phase 2B:**
We will transition to Phase 2B ONLY IF the alternative representation demonstrates robust, statistically supported separability between stochastic and deterministic processes without causing stochastic benchmark processes (White Noise, Pink Noise, AR(1)) to exhibit geometric characteristics that substantially reduce their separation from deterministic benchmark systems. The decision will be based on the convergence of evidence across the pre-registered primary and secondary endpoints, rather than on any single statistical measure or predefined numerical threshold.

## Data Integrity Check
Before executing the primary analysis, the generated dataset must pass the following integrity criteria:

| Data Integrity Check | Acceptance criterion |
| :--- | :--- |
| **Number of realizations** | Exactly 100 per signal $\times$ parameter combination |
| **Effective length** | Matches $N_{eff} = N - (m-1)\tau$ |
| **Missing values** | None after embedding |
| **Failed ICCS runs** | 0 (or explicitly documented) |
| **Random seed logging** | Present and reproducible |
| **Software version** | ICCS v0.3.1 (frozen) |

## Evaluated Signals (N=100 realizations each, N=1000 points)
1. `gaussian_white_noise` — Purely stochastic benchmark with no temporal memory.
2. `pink_noise` — Stochastic benchmark exhibiting long-range temporal dependence.
3. `ar1_05` and `ar1_09` — Intermediate stochastic benchmarks with short-range autoregressive dependence ($\phi=0.5$ and $\phi=0.9$). These processes serve as intermediate controls occupying the continuum between memoryless stochastic processes and deterministic chaotic dynamics.
4. `lorenz` — Deterministic chaotic benchmark.

## Parameter Sweep
- Baseline: `m=1`, `tau=1`
- Delay Embedding: `m \in [2, 3, 4, 5]`, `tau \in [1, 5, 10]`
- **Effective Length ($N_{eff}$)**: Tracked for all configs to ensure any shift in baseline metrics (M, TE) is contextualized by sample size reduction.

*The selected parameter range is intended to sample a representative region of practical embedding configurations rather than to optimize performance. No attempt will be made to identify globally optimal embedding parameters within this study.*

## Exploratory Analyses
Any analyses not explicitly specified in this protocol (including additional parameter combinations, alternative embedding methods, post hoc subgroup analyses, or modified benchmark comparisons) will be reported separately as exploratory analyses and will not be used as primary evidence for the Phase 2B decision.

## Pre-registered Statistical Protocol

**Primary endpoint**
Stability of geometric discrimination across the investigated embedding parameter space, evaluated jointly across benchmark systems.

**Secondary endpoints**
The secondary analyses quantify different aspects of class separability and statistical robustness. Agreement across these complementary measures is interpreted as stronger evidence than any individual statistic. These analyses are complementary and address different statistical properties of class separation (ranking performance, standardized effect size, distributional overlap, and statistical significance).

For key signal pairs (e.g., White vs Lorenz, Pink vs Lorenz, AR1 vs Lorenz, White vs Pink) across all parameters, we compute:

| Metric | Scientific Interpretation |
| :--- | :--- |
| **ROC AUC** (w/ 95% Bootstrap CI) | The probability that the metric correctly ranks a randomly selected realization from one benchmark class above a randomly selected realization from the comparison class. Values approaching 1 indicate strong separability between the evaluated classes. |
| **Cohen's *d*** (w/ 95% Bootstrap CI) | Standardized effect size describing the magnitude of the separation between benchmark distributions. It is interpreted together with confidence intervals and complementary statistical measures rather than as standalone evidence. |
| **Overlap Coefficient** | Quantifies the degree of overlap between empirical distributions. Lower overlap is consistent with greater geometric discrimination. |
| **Permutation Test** (*p*-value) | Assesses whether the observed group difference is larger than expected under random label permutations. |

**Sensitivity Analysis**
The conclusions of Phase 2A will be considered robust only if they remain qualitatively unchanged across reasonable variations of embedding parameters $(m,\tau)$ and across independent stochastic realizations. Sensitivity analyses are considered descriptive and are used to characterize the robustness of the representation rather than to identify an optimal embedding configuration. Large qualitative changes resulting from small variations of embedding parameters will be interpreted as evidence of parameter sensitivity rather than improved representation.

**Phase 2A will be considered successful only if the overall body of evidence indicates a stable region of geometric discrimination across the investigated parameter space, while preserving the expected qualitative ordering of the benchmark systems (i.e., stochastic benchmark processes should remain distinguishable from deterministic chaotic dynamics across the investigated parameter space). Evidence of substantial parameter sensitivity or inconsistent behavior across the pre-registered statistical analyses will be interpreted as a limitation of the representation rather than as support for Phase 2B. No single statistical measure will be treated as sufficient evidence in isolation. A negative outcome (failure to identify a stable region of discrimination) will be interpreted as a scientifically informative boundary of the current representation rather than evidence of experimental failure.**
