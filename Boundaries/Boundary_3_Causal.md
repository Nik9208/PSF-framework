# Causal vs Predictive Divergence

## Overview
This test challenges the foundational assumption that predictive structure reliably maps to causal structure. We examine whether systems with identical predictive scores (MI forward) but fundamentally different causal graphs yield identical structural scores under the current ICCS implementation.

## Setup

We generate three linear stochastic systems, tuning parameters such that $MI(X_t; Y_{t+1})$ is identical across all three.

### System A: Direct Causal
$X_{t+1} = a X_t + \epsilon_x$
$Y_{t+1} = b X_t + \epsilon_y$
(Directed influence: $X_t \rightarrow Y_{t+1}$)

### System B: Common Driver
$Z_{t+1} = a Z_t + \epsilon_z$
$X_{t+1} = b Z_t + \epsilon_x$
$Y_{t+1} = b Z_t + \epsilon_y$
(Common cause: $Z \rightarrow X$, $Z \rightarrow Y$. No direct link between X and Y).

### System C: Reverse Predictive Trap
$Y_{t+1} = a Y_t + \epsilon_y$
$X_{t+1} = b Y_t + \epsilon_x$
(Directed influence: $Y_t \rightarrow X_{t+1}$, but we still measure $MI(X_t; Y_{t+1})$).

## Conditional Information Proxy

Because exact continuous CMI estimation is non-trivial, we use a residual-based approximation.

**Procedure:**
1. Regress $X_t$ on $Z_t$: $X_t = f(Z_t) + r_x$
2. Regress $Y_{t+1}$ on $Z_t$: $Y_{t+1} = g(Z_t) + r_y$
3. Estimate: $MI(r_x ; r_y)$ as a proxy for $I(Y_{t+1}; X_t | Z_t)$

**Limitation:**
This is a linear conditional independence approximation. It is not a general estimator of continuous CMI.

## Boundary Condition

If $ICCS_A \approx ICCS_B \approx ICCS_C$ 
while simultaneously showing:
- different causal graphs
- different directionality (MI forward vs MI reverse)
- different conditional dependence (CMI proxy)

Then a boundary is found: 
**Prediction $\neq$ Causation** and predictive structure alone does not identify causal structure without additional constraints.
