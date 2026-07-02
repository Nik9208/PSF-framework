# v0.3 Baseline Discrimination Study

## Objective
Evaluate what structural information remains unrepresented by standard scalar and low-dimensional baseline metrics compared to the ICCS feature space. This study establishes the specific analytical positioning of the PSF framework.

## Methodology
- **Dataset:** C-MAPSS FD001 (20 engines)
- **Windows:** Early (0-33%) vs Late (66-100%)
- **Fixed Representation:** X=s9, Y=s4, Z=s3 (unbiased, data-driven baseline)

### Evaluated Baselines:
1. **Scalar Variance:** $Var(X)$, $Var(Y)$, $Var(Z)$
2. **Correlation:** Absolute Pearson correlation $|corr(X,Y)|$, $|corr(X,Z)|$
3. **Entropy:** Histogram-based Shannon Entropy (30 bins, intentionally simple estimator)
4. **Mutual Information:** k-NN continuous Mutual Information (nonlinear association)
5. **PCA Latent Variance:** Explained variance ratio of PC1 and PC2

---

## Empirical Observations

### 1. Limited Sensitivity of Scalar Information (Entropy)
Despite severe system degradation, scalar uncertainty (Shannon Entropy) remained almost completely flat ($H_X \approx 2.97 \rightarrow 3.04$). Simple discrete entropy shows limited sensitivity to changes in deterministic structure because it only measures the static probability distribution of the amplitude, and does not explicitly encode temporal ordering or state-space geometry.

### 2. Scalar Amplification Without Structural Decomposition
Variance increased massively ($Var(X): 17 \rightarrow 445$) and linear correlation jumped ($corr_{xy}: 0.10 \rightarrow 0.57$). However, these metrics conflate noise, mean-shifting, and amplitude scaling. They confirm that the signal is "changing", but do not directly separate underlying structural changes (such as memory vs coupling).

### 3. Geometry Compression Under PCA
In the Early phase, the leading principal component captured $\approx 39\%$ of the variance. In the Late phase, this jumped to $\approx 70\%$. While PCA successfully detects that the system collapses into a lower-dimensional linear manifold as it degrades, PCA explicitly enforces linear orthogonality, and does not preserve explicit directional dependency estimates between original channels.

---

## Structural Sensitivity Matrix

The following matrix defines the positioning of ICCS relative to classical baselines. Rather than ranking methods by "performance", it identifies the specific types of information not represented by the baselines.

| Method      | Type                 | Captures                                |
| ----------- | -------------------- | --------------------------------------- |
| Variance    | scalar               | amplitude                               |
| Entropy     | scalar information   | uncertainty                             |
| Correlation | pairwise             | static dependency                       |
| MI          | nonlinear dependency | association                             |
| PCA         | latent projection    | compressed geometry                     |
| ICCS        | dynamic structure    | memory + directed dependency + geometry |

### Information not represented by the baseline:
- **Variance / Correlation / MI:** Do not capture temporal memory ($M(k)$) or geometric complexity invariant to scale ($D_{local}$).
- **Entropy:** Does not capture multi-dimensional dependencies or temporal organization.
- **PCA:** Reduces nonlinear cross-channel interaction dynamics under linear projection.
- **ICCS Advantage:** Within the evaluated representations and in this evaluation setting, ICCS provides explicit separation of temporal memory, local state-space geometry, and directed dependency structures into decoupled, measurable axes.
