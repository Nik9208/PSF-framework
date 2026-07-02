# Welcome to PSF / ICCS v1.0

If you are opening this repository for the first time, this file will help you quickly understand what this project is about and how to start.

You do not need deep knowledge of machine learning or information theory. The core idea can be understood intuitively.

---

# 🧠 What is this project?

PSF / ICCS is a research framework for analyzing the structure and dynamics of multivariate time series.
**ICCS is a framework for discovering and validating latent structure in time-dependent systems.**

Instead of asking:

> "What is the value of this system?"

we ask:

> "What structural behavior does this system exhibit over time?"

---

# 📌 The Main Problem

In many real-world datasets (sensors, finance, biology, climate systems), we usually reduce complexity to a single number:

- entropy
- variance
- complexity score
- risk index

But a single number cannot distinguish fundamentally different systems.

Two systems can look identical numerically but behave completely differently over time.

---

# 🧠 Core Idea of ICCS

ICCS represents a system as a **multi-dimensional regime structure**, not a single metric.

Instead of outputting one value, it describes:

- how states are organized
- how they transition over time
- how stable those transitions are
- how structure changes under stress

---

# 🏗 How ICCS works (3 layers)

## 1. Representation Layer
Transforms raw time series into structured latent regimes.

Includes:
- structural decomposition
- regime extraction
- temporal orientation analysis

---

## 2. Dynamics Layer
Models how regimes evolve over time.

Includes:
- transition graphs
- regime stability estimation
- manifold geometry and curvature analysis

---

## 3. Control & Learning Layer
Analyzes and adapts the structure itself.

Includes:
- causal risk field estimation
- collapse prediction
- self-optimizing representation learning

---

# 🧪 How we test whether structure is real

ICCS is tested against:

- synthetic dynamical systems (Logistic map, Lorenz system)
- noise and shuffled surrogates
- random processes
- real-world proxy datasets

And compared to standard baselines:

- HMM models
- spectral embeddings (Koopman-style)
- change-point detection methods
- clustering-based methods (PCA + GMM, UMAP + HDBSCAN)

---

# 🔍 What makes ICCS different?

Instead of detecting only:

- clusters
- anomalies
- or change points

ICCS builds a **structured map of regime behavior over time**, including:

- stability of regimes
- transitions between regimes
- structural deformation of the system itself
- predictive risk of collapse

Crucially, **ICCS actively tests whether the structure is real** or just a statistical hallucination by subjecting it to strict falsification harnesses.

---

# 📊 What you get as output

Instead of a single score, ICCS produces:

- regime structure
- transition graph
- stability metrics
- curvature / instability maps
- causal risk signals

---

# ⚠️ Important limitations

ICCS is a research framework.

It does NOT:

- guarantee causal discovery
- replace physical modeling
- provide absolute truth about system structure

It is a tool for exploring structural hypotheses about data.

---

# 🚀 How to start

Run the full pipeline:

```bash
cd Experiments/v0.4/phase4
python run_all.py
```

Or explore components in:

* `experiments/` — benchmarking and validation
* `iccs_v4/` — core framework
* `results/` — generated outputs

---

# 📌 Summary

ICCS helps answer:

> "What structure is hidden in time-dependent data, and how does it evolve?"

rather than:

> "What is the next value?"
