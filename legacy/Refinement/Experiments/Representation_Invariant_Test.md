# Representation-Invariant Refinement Test

## Objective
Test whether the currently accepted Dynamics-aware candidate (Memory Profile $M(X)$ and $P(k)$) is robust against the adversarial representations identified in Boundary #2. 

## Hypothesis
If $M(X)$ is purely a structural property, it should be invariant to bijective transformations that preserve all information.
However, because operational MI relies on geometric density estimation (e.g. kNN), we expect the naive implementation of $M(X)$ to fail this test.

## Transformations
A base 2D nonlinear oscillator will be subjected to:
1. Original (Identity)
2. Additive Numerical Noise (Identity Test to establish $\varepsilon$)
3. Linear Scaling
4. Rotation ($\pi/4$)
5. Permutation (Axis Swap)
6. Cubic Bijection ($x \rightarrow x + x^3$)

## Representation Invariance Criterion
A candidate passes if:
$\Delta M = \frac{|M(T(X)) - M(X)|}{M(X)} < \varepsilon$

and the Profile Distance is comparably small:
$\Delta P = \frac{1}{K} \sum_{k=1}^{K} \frac{|P(k) - P_{base}(k)|}{P_{base}(k)} < \varepsilon$

where $\varepsilon$ is determined empirically from the "Numerical Noise" identity test.
If $\Delta M > \varepsilon$ for valid bijections, a new boundary for ICCS v1.1 is found, necessitating invariant estimators (e.g. Copula ranks or TDA).
