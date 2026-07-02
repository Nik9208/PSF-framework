# Robustness Study Summary (v0.1.1)

> [!NOTE]
> This summary synthesizes the findings from `robustness_raw.csv` and the generated plots. 
> Ensure you have run `python Experiments/robustness_evaluation.py` to generate the latest empirical data before relying on these conclusions.

## 1. Noise Robustness (Experiment 1)
*Analysis of how structural properties degrade under relative Gaussian noise at N=5000.*

- **Geometry ($D_{local}$)**: Exhibited remarkable empirical stability. Across all noise levels (0% to 20%) and all systems, $D_{local}$ remained firmly within the $1.11 - 1.13$ range. The local topological structure was preserved despite observational perturbations.
- **Memory ($M$)**: Demonstrated smooth, monotonic degradation. For instance, the Lorenz system's memory dropped progressively from $20.06$ (0% noise) to $9.84$ (20% noise), reflecting the expected washing out of deterministic predictability.
- **Causality ($TE/CMI$)**: Exhibited system-dependent sensitivity. For chaotic systems (Lorenz), $TE$ degraded abruptly, collapsing from $0.64$ to $0.00$ by 5% noise. However, for linearly coupled stochastic systems, $TE$ proved highly resilient, maintaining a strong signal ($\approx 0.22$) even at 20% noise.

## 2. Sample Size Convergence (Experiment 2)
*Analysis of minimum data requirements to achieve stable structural signatures.*

- **$M(k)$ Convergence**: Stabilized rapidly, yielding consistent profiles even at lower sample sizes.
- **$D_{local}$ Convergence**: Achieved stability moderately fast, holding its geometric estimate consistently above $N=1000$.
- **Causal Fingerprint Convergence**: As expected, k-NN density estimations for $TE$ required larger sample sizes to minimize variance and accurately capture the conditional distributions.

## 3. Boundary Preservation (Experiment 3)
*Analysis of whether the BVP separation holds despite absolute metric degradation.*

**Findings**:
- **Absolute Gap**: Remained highly stable. The causal system maintained $TE \approx 0.22$, while the predictive mimic maintained $TE \approx 0.00$ across the entire noise sweep.
- **Relative Gap**: Stayed exceptionally high (between $0.90$ and $1.00$), far above the $0.1$ failure threshold.
- **Failure Boundary**: The causal separation boundary **did not fail** within the tested operational domain (up to 20% relative noise). The relational gap is significantly more robust than absolute predictive measurements (like $M(k)$).

## 4. Hyperparameter Stability (Experiment 4)
*Analysis of structural feature variance under different k-NN topologies ($k \in [5, 10, 20, 50]$).*

- **$k$-variance Impact**: The structural ordering was fully preserved regardless of hyperparameter choice. Across $k \in \{5, 10, 20, 50\}$, the assertion $TE_{causal} > TE_{mimic}$ held true universally, confirming that BVP separation is invariant to local topological definitions within reasonable bounds.
