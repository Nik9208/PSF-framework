# Publication Outline: The Boundary Validation Protocol (BVP)

## 1. Problem
* Limitations of one-dimensional predictive metrics in complex systems analysis.
* Why evaluating the "complexity" of structural representations requires stress-testing the estimators themselves.
* **Contributions:**
  - **Methodological contribution:** The Boundary Validation Protocol (BVP), an iterative methodology for developing structural complexity measures through systematic falsification.
  - **Empirical contribution:** ICCS v1.1, a boundary-validated structural representation.
  - **Experimental contribution:** A benchmark suite of four validated boundary conditions isolating distinct structural ambiguities.

## 2. The Boundary Validation Protocol (BVP)
* **Epistemological Stance:** A complexity metric should be regarded as adequate only with respect to the currently validated boundary suite rather than universally complete.
* **Definition (Boundary):** A boundary is a controlled benchmark in which two or more systems are intentionally constructed so that a candidate metric produces an ambiguous or potentially misleading evaluation despite underlying structural differences.
* **Requirements for a valid boundary:**
  - Isolate a single ambiguity class.
  - Minimize unrelated confounding factors.
  - Admit reproducible generation.
  - Produce quantitative pass/fail criteria.
* **Formal Algorithm:**
  ```text
  Input: structural metric M
  repeat
      construct boundary B
      if M fails on B:
          identify ambiguity class A
          introduce descriptor D orthogonal to M
          redefine metric M
  until M passes all currently defined boundary conditions
  ```
* Each boundary isolates a distinct source of structural ambiguity:
  - **Temporal Ambiguity Boundary:** Equal single-step mutual information, different global dynamics.
  - **Representation Ambiguity Boundary:** Sensitivity of raw predictive information to state-space geometry and observer coordinates.
  - **Causal Ambiguity Boundary:** Inability of pure prediction to distinguish direct influence from common drivers.
  - **Aggregation Ambiguity Boundary:** Testing whether scalar reduction destroys multidimensional structural profiles.
* **Scope and Limitations of the current Boundary Set:**
  - The proposed boundaries are not claimed to be exhaustive.
  - They constitute the first validated benchmark suite addressing four independent ambiguity classes.
  - Additional boundaries (e.g., multiscale, partial observability, nonstationarity) remain open for future work.

## 3. Case Study: Iterative Refinement of ICCS
* Applying the BVP to systematically derive a boundary-validated structural representation.
* **Definition (Orthogonal Descriptor):** A descriptor is considered orthogonal if it resolves an ambiguity that cannot be resolved by the previously accepted descriptor set under the validated boundary suite. Functional independence rather than linear algebraic orthogonality.
* **Dynamics-aware:** Multi-step predictive memory profile ($M(k)$) to resolve Temporal Ambiguity.
* **Representation-invariant:** Local intrinsic dimension ($D_{local}$) to resolve Representation Ambiguity.
* **Causal-aware:** Causal Fingerprint ($TE_{+}$, $TE_{-}$, $CMI$) to resolve Causal Ambiguity.

## 4. Architecture of ICCS v1.1
* **Structural Feature Space:** $S(X) = [M(k), D_{local}, TE_{forward}, TE_{reverse}, CMI]$
* **Design Principle:** The components are intentionally maintained as independent descriptors. Aggregation is treated as a secondary operation rather than the definition of structural complexity itself.
* **Aggregation Analysis:** Evaluating alternative aggregation strategies against the Aggregation Ambiguity Boundary.

## 5. Extensive Evaluation and Generalization
* **Sensitivity & Robustness Analysis:** Evaluating the stability of $S(X)$ across varying sample sizes, noise levels, estimator hyperparameters, and random initializations across 100-1000 independent runs.
* **Generalization Benchmarks:** Validating the BVP and ICCS on unseen data classes, including out-of-distribution chaotic systems, non-linear AR models, and empirical real-world time series.

## 6. Ablation Study
* Step-by-step demonstration of the necessity of each structural layer:
  - $M$ passes Temporal, fails Representation, Causal, Aggregation
  - $M + D_{local}$ passes Temporal, Representation, fails Causal, Aggregation
  - $M + D_{local} + TE$ passes Temporal, Representation, partially Causal, fails Aggregation
  - Full vector $S(X)$ preserves structural separability across all tested boundaries.

## 7. Benchmark Evaluation
* **Single-metric baselines:**
  - Mutual Information (MI)
  - Predictive Information (PI)
  - Transfer Entropy (TE)
  - Intrinsic Dimension (ID)
* **Structural-analysis baselines:**
  - Recurrence Quantification Analysis (RQA)
  - Permutation Entropy
  - Other applicable complexity measures
* Demonstrating the additive value of the unified structural feature space over isolated metrics.

## 8. Complexity and Theoretical Analysis
* **Theoretical Properties:** Formal properties of each estimator (e.g., non-negativity of memory profile, representation invariance of local dimension under tested transformations, asymmetry of TE proxy).
* **Computational Complexity:** Big-O analysis of memory and time requirements for the full feature space evaluation to demonstrate scalability to large datasets.

## 9. Threats to Validity
* Reliance on linear proxies for TE and CMI.
* Evaluation currently restricted to a limited set of test systems.
* Dependence of certain estimates (e.g., local intrinsic dimension) on specific hyperparameters.
* Absence of strict theoretical guarantees for all empirical components.
* The imperative to extend validation to high-dimensional, noisy real-world datasets.

## 10. Discussion
* Conditions under which structural profiling is preferable to a single complexity score.
* **Open Research Question:** The present study found that the tested scalar aggregation schemes failed to preserve all validated structural distinctions. This failure does not imply that scalar representations are impossible, only that the tested aggregation schemes were insufficient. Whether a different class of aggregation can achieve this without information loss remains an open research question.
* Future directions for non-linear proxy validation in the causal layer.

## 11. Reproducibility
* Public Repository with open-source code.
* Exact Boundary definitions and experimental scripts.
* Random seeds and configuration files.
* Detailed statistical protocol for all evaluations.
