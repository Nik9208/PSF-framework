# ICCS v1.0 — Information-Theoretic Regime Analysis Framework

![status](https://img.shields.io/badge/status-research--prototype-blue)
![version](https://img.shields.io/badge/version-1.0-green)
![ICCS](https://img.shields.io/badge/framework-ICCS-orange)

ICCS (Information-Theoretic Complex Systems framework) is an experimental system for analyzing temporal dynamics through regime extraction, transition topology, and stability-aware spectral embeddings.

It provides a full pipeline:

> raw time series → latent regimes → transition graph → instability metrics → causal risk field → control/meta-optimization

---

## 🚀 Quick Start

```bash
cd Experiments/v0.4/phase4
python run_all.py
```

This will:
* run falsification tests
* compute regime structure
* generate transition graphs
* evaluate baselines
* produce final figures

---

## 💡 Example Output

ICCS produces:
- Regime A → stable low-dimension structure
- Regime B → high curvature instability zone
- Transition entropy → increasing before collapse
- Causal risk → spike detected before regime shift

---

## 🧠 Core Idea

Instead of treating time series as sequences of values, ICCS treats them as:

> structured transitions between latent regimes embedded in a dynamical manifold

The system combines:
- spectral decomposition (Koopman-like embeddings)
- clustering of latent regimes
- transition graph modeling (Markov structure)
- curvature-based instability estimation
- causal risk propagation
- control and meta-learning layers

---

## 🏗 Architecture (3 Layers)

### 1. Representation Layer
- SCO (Structural Conflation Operator)
- RSO (Regime Stability Operator)
- TOO (Temporal Orientation Operator)
→ transforms raw signals into structured latent space

### 2. Dynamics Layer
- Regime Geometry Reconstruction
- Transition Graph Construction
- Manifold Curvature Estimation
→ extracts temporal and topological structure

### 3. Control Layer
- Causal Regime Dynamics
- Anti-collapse policy synthesis
- Self-optimizing regime compiler
→ predicts instability and modifies representation space

---

## 📁 Project Map

ICCS v1.0 consists of:

**Core:**
- `iccs_v4/` (representation + dynamics + control)

**Experiment Layer:**
- `experiments/` (benchmarks + falsification + visualizer)

**Output:**
- `results/` (figures + logs)

**Entry Point:**
- `run_all.py`

**Documentation:**
- `docs/` (specification, validation plan, paper draft)

---

## 🧪 Evaluation Framework & Results

ICCS is tested against standard baselines (HMM proxy, Koopman spectral proxy, Change-point detection, PCA+GMM).

**Key Results:**
- Strong alignment with Koopman spectral dynamics.
- Clear separation from change-point detection methods.
- Falsification tested: Fails gracefully on noise, preserves structure only when temporal ordering exists.

---

## ⚠️ What this is NOT

ICCS is NOT:
- a prediction system
- a black-box AI model
- a causal discovery guarantee
- a production-ready ML pipeline

It is a structural analysis framework for dynamical systems.

---

## 📌 Scientific Position

ICCS can be interpreted as:

> a regime-based extension of Koopman spectral analysis with integrated stability and causal risk estimation

---

## 📄 Citation

If you reference this work:

```text
ICCS v1.0: Regime-Based Information-Theoretic Analysis of Dynamical Systems
```

---

## 📜 License
Research / experimental use only
