# Dynamics-Aware Refinement Test

## Objective
To replace the naive $ICCS_{1.0}$ assumption that structural predictability can be captured by $MI(X_t; X_{t+1})$ alone.
We aim to construct a feature vector (Dynamics Fingerprint) that successfully distinguishes dynamically diverse systems that possess identical short-term predictability.

## Hypothesis
The candidate feature vector $F(X) = [P(1), ..., P(10), RR, DET]$ will successfully separate chaotic, stochastic, and periodic dynamics, whereas $MI(k=1)$ alone fails.

## Systems Tested

All systems will be tuned such that $MI(X_t; X_{t+1}) \approx const$.

### 1. Lorenz Attractor
- **Nature:** Structured chaotic
- **Expected Profile:** High determinism (DET), decaying but non-zero memory profile.

### 2. AR(1) Process
- **Nature:** Stochastic memory
- **Expected Profile:** Low determinism (DET), exponentially decaying memory profile.

### 3. Noisy Periodic Oscillator
- **Nature:** Simple deterministic
- **Expected Profile:** High determinism (DET), oscillating/non-decaying memory profile.

## Success Criterion
```
ICCS v1.0: Lorenz ≈ AR ≈ Oscillator
Dynamics Fingerprint v1.1: Lorenz ≠ AR ≠ Oscillator
```
If the feature vector robustly separates the three domains, we will confirm it as the Dynamics-aware component of ICCS v1.1.
