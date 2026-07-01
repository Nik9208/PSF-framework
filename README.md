# Boundary Validation Protocol (BVP)

An iterative methodology for constructing and validating structural complexity representations.

**Case study:**
ICCS v1.1 (Information-theoretic Causal Complexity Score)

## Core contributions

* **Boundary Validation Protocol (BVP)**
* **ICCS v1.1 case study**
* **Four validated boundary benchmarks**
* **Open-source experimental framework**

## Overview
Evaluating the "complexity" of structural representations requires stress-testing the estimators themselves. 
This repository introduces the **Boundary Validation Protocol (BVP)**, an iterative methodology for developing structural complexity measures through systematic falsification against specifically constructed boundary conditions.

Rather than searching for a universal scalar metric of complexity, the BVP operates on the epistemological stance that a complexity metric is never considered universally complete. Its validity is always provisional with respect to the current boundary suite.

## Why BVP?

**Traditional workflow:**
`metric` $\rightarrow$ `benchmark`

**BVP workflow:**
`metric` $\rightarrow$ `boundary test` $\rightarrow$ `failure` $\rightarrow$ `new descriptor` $\rightarrow$ `repeat`

By intentionally stress-testing metrics against isolated structural ambiguities, the BVP forces the evolution of multidimensional, boundary-validated feature spaces rather than relying on brittle scalar formulas.

## Repository Structure

- `docs/`: Core methodology documentation.
  - `BVP_Protocol.md`: The formal BVP algorithm and epistemology.
  - `Definitions.md`: Formal definitions of Boundaries, Ambiguity Classes, and Orthogonal Descriptors.
  - `ICCS_v1.1_Architecture.md`: The structural feature space derived via BVP.
  - `Publication_Outline.md`: The outline of the research paper.
- `Boundaries/`: Formal definitions of the four isolated ambiguity boundaries.
- `Experiments/`: Python validation scripts executing the BVP stress-tests.
- `Results/`: Empirical results of the ICCS v1.1 case study passing the boundaries.
- `examples/`: Simple usage demos for the framework.
- `legacy/`: Archive of the evolutionary iterations and previous metric configurations.

## Reproducibility
This repository aims to provide all materials required to reproduce the reported experiments, including boundary definitions, experimental scripts, configuration files, and statistical evaluation procedures.
