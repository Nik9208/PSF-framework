# C-MAPSS Experiment 3: Noise Boundary

## Objective
Evaluate the robustness of ICCS components under controlled observational noise in real-world multivariate sensor trajectories. We aim to determine how differential degradation profiles across ICCS components react to deteriorated measurement quality, measuring the boundary where structural signatures are lost.

## Methodology
- **Dataset**: C-MAPSS FD001 (First 20 engines).
- **Phases**: `Early` (0-33%) and `Late` (66-100%).
- **Channels**: Fixed baseline ($X=s9, Y=s4, Z=s3$).
- **Noise Injection**: Relative Gaussian noise added to raw sensors: $X_{noise} = X + \epsilon \cdot \sigma_X$ with $\epsilon \sim \mathcal{N}(0, \alpha)$ and $\alpha \in \{0.0, 0.05, 0.10, 0.20\}$.
- **Repeats**: 5 random seeds per engine/phase/noise combination.

## Empirical Findings (Mean Across Engines and Repeats)

| Phase | Noise Level | $M(k)$ | $D_{local}$ | $TE_{forward}$ | $TE_{reverse}$ | $CMI$ |
|-------|-------------|--------|-------------|----------------|----------------|-------|
| Early | 0%          | 0.116  | 3.365       | 0.024          | 0.021          | 0.017 |
| Early | 5%          | 0.114  | 3.365       | 0.028          | 0.023          | 0.020 |
| Early | 10%         | 0.107  | 3.342       | 0.030          | 0.032          | 0.017 |
| Early | 20%         | 0.114  | 3.349       | 0.022          | 0.025          | 0.026 |
|-------|-------------|--------|-------------|----------------|----------------|-------|
| Late  | 0%          | 5.523  | 2.988       | 0.039          | 0.041          | 0.221 |
| Late  | 5%          | 5.433  | 2.986       | 0.044          | 0.038          | 0.212 |
| Late  | 10%         | 5.069  | 2.985       | 0.051          | 0.043          | 0.197 |
| Late  | 20%         | 4.169  | 3.015       | 0.046          | 0.041          | 0.173 |

## Interpretation & Conclusions

1. **Geometric Stability Under Noise**

The local geometric estimate ($D_{local}$) remains comparatively stable within each degradation phase across increasing noise levels. This suggests that the local structure captured by the ICCS representation is less sensitive to additive Gaussian observational noise than other components.

2. **Memory Attenuation**

The memory component ($M(k)$) decreases gradually under increasing noise in the Late degradation phase. Since injected Gaussian noise does not contain temporal structure, the observed change is consistent with attenuation of temporal predictability.

3. **Dependency Signature Persistence**

The dependency estimates ($TE$ and $CMI$) change with increasing noise but retain a substantial difference between Early and Late degradation phases. This indicates that multivariate dependency patterns remain detectable under moderate observational degradation.
