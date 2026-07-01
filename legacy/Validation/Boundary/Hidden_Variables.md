# Hidden Variables Test

## Overview
Can a system have hidden states that alter the available predictive structure such that the observed structure is false?

## Setup
True system: $X_t = f(X_{t-1}, H_t)$
Observer builds: $\hat{\Phi}(X)$

## Failure condition
If $I(\hat{\Phi}; X_{future})$ is high, but $I(\hat{\Phi}; H)$ is low, PSF only sees a projection.
Falsification: There exist hidden variables that yield a different, stable predictive manifold.
