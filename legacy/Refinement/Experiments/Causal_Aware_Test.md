# Causal-Aware Refinement Test

## Objective
To test whether the Causal Fingerprint $C(X,Y)$ can distinguish between direct causality, reverse causality, and common driver scenarios under conditions of predictive equivalence.

## Systems
| System | Structure | Meaning |
|---|---|---|
| A | $X \rightarrow Y$ | True causation |
| B | $Z \rightarrow X, Z \rightarrow Y$ | Hidden common driver |
| C | $Y \rightarrow X$ | Reversed causation |
| D | Temporal matched | Predictive mimic |

All systems are matched such that their primary predictive mutual information $MI$ is approximately equal.

## Causal Fingerprint
$C(X,Y) = [TE_{X \rightarrow Y}, TE_{Y \rightarrow X}, CMI(X;Y|Z)]$

Where $TE$ and $CMI$ are estimated using a residual-based linear proxy (v0.1):
- $TE_{X \rightarrow Y}$: $MI(X_{t-1}; Y_t - E[Y_t|Y_{t-1}])$
- $TE_{Y \rightarrow X}$: $MI(Y_{t-1}; X_t - E[X_t|X_{t-1}])$
- $CMI(X;Y|Z)$: $MI(X_t - E[X_t|Z_{t-1}]; Y_t - E[Y_t|Z_{t-1}])$

## Success Criterion

The causal fingerprint should preserve causal asymmetry under predictive equivalence.

A successful candidate satisfies:
$Prediction(A) \approx Prediction(B) \approx Prediction(C) \approx Prediction(D)$

while:
$CausalFingerprint(A) \neq CausalFingerprint(B) \neq CausalFingerprint(C) \neq CausalFingerprint(D)$
