# 👋 Welcome to PSF/ICCS

If you are opening this repository for the first time, this file will help you quickly understand what this project is about, why it is needed, and where to start.

You do not need to know information theory, statistics, or machine learning to understand the project. Here we explain the core idea in plain words.

---

# What is this project?

PSF/ICCS is a research tool for analyzing the structure of multivariate time series.

Simply put, it helps answer the question:

> **Which system properties are detectable from the observed data, and which appear only due to the chosen method of analysis?**

In many domains (equipment sensors, biological signals, climate data, etc.), data looks very complex.

Usually, researchers try to describe it with a single numerical characteristic:

* entropy;
* variance;
* complexity index;
* a single quality metric.

But a single number often hides differences between completely different systems.

This is exactly the problem this project tries to solve.

---

# The Main Idea

Instead of a single "complexity" score, we consider several independent characteristics of the system's structure.

For example, two systems might have the same entropy, but:

* the first one has strong memory;
* the second one has almost no memory;

or

* the first one contains strong dependencies between variables;
* the second one consists of almost independent processes.

If you use only one number, these differences might disappear.

Therefore, ICCS describes the system across several dimensions simultaneously.

---

# Why is the project named PSF/ICCS?

**PSF** refers to the original research framework, which sets the general validation paradigm. 

**ICCS** (Information-Theoretic Structural Complexity Space) is the specific multidimensional feature space (structural complexity profile) evaluated within it. 

This separation allows for testing other data representations in the future under the same BVP validation approach.

---

# What is ICCS?

ICCS stands for

**Information-Theoretic Structural Complexity Space**

Despite the complex name, the idea is very simple.

ICCS is not a single metric.

It is a system profile.

Instead of answering

> "Complexity = 4.8"

we get a description of several properties at once.

Currently, ICCS includes three main directions of analysis.

---

## 1. Memory

Answers the question:

> How much does the past help predict the future?

If the system's state heavily depends on its previous states, memory is considered high.

If the past says almost nothing about the future, memory is low.

Example:

A pendulum has high memory.

A sequence of random numbers has practically none.

---

## 2. Geometry

Answers the question:

> How is the system's state space structured?

Imagine that every state of the system becomes a point.

Sometimes all points lie almost on a line.

Sometimes they form a surface.

Sometimes they fill a complex multidimensional region.

Geometry estimates exactly this hidden data organization.

---

## 3. Dependency

Answers the question:

> To what extent are different parts of the system statistically related or provide predictive information about each other?

For example:

engine temperature

↓

pressure

↓

vibration

If a change in one variable helps explain a change in another, this is reflected in the Dependency component.

---

# What is BVP?

BVP stands for

**Boundary Validation Protocol**

It is not an algorithm.

It is a validation method.

It answers the question:

> Can we trust the chosen data representation?

To do this, the system is deliberately subjected to various changes.

For example:

* noise is added;
* the method of data representation is changed;
* different stages of system operation are analyzed.

After each change, we check:

Which properties are preserved?

Which disappear?

If a certain characteristic stops distinguishing between different systems after even a small change in the data, it means we have found the boundary of its applicability.

This is exactly why the method is called Boundary Validation.

---

# Why do BVP and ICCS exist together?

You can imagine their roles like this.

BVP answers:

> How to test?

ICCS answers:

> What to measure?

They complement each other.

---

# What can be analyzed?

The project is designed to analyze multivariate time series.

For example:

* sensor data;
* industrial equipment;
* physiological signals;
* climate observations;
* experimental measurements;
* financial time series.

The main condition is that the data must represent a sequence of observations over time.

---

# What is used as an example?

The main validation of the project is performed on two types of data.

## Synthetic Systems

They allow creating controlled situations where it is known in advance which structural properties should be preserved.

This helps to understand how different components of ICCS behave.

---

## NASA C-MAPSS

This is an open dataset simulating the degradation of aviation engines.

It is used as a real-world example of how observed structural signatures change during degradation.

Important to understand:

The project is not designed to predict the remaining useful life of an engine.

The data is used as a convenient real-world environment to test the behavior of ICCS and BVP.

---

# What will you get after the analysis?

Instead of a single score, you will get a structural profile.

For example:

```
Memory      high
Geometry    stable
Dependency  decreasing
```

or

```
Memory      decreasing
Geometry    almost unchanged
Dependency  drops sharply
```

Such a profile allows you to understand **exactly which system properties are changing**, not just that the "complexity became lower".

---

# Do I need to understand the math?

No.

To get familiar with the project, it is enough to understand the meaning of the components.

All mathematical details are in the manuscript and source code.

If you want to use the ready-made experiments, knowing the exact formulas is not required.

---

# Where to start?

If you want to get familiar with the project:

1. Read this file.

2. Then open `README.md`.

For reproducible experiments, use the provided environment and scripts described in `REPRODUCIBILITY.md`.

If you are interested in the theory — open `paper/manuscript.md`.

---

# Project Limitations

It is important to understand that PSF/ICCS is a research tool.

It **does not try to automatically determine the "true complexity" of any system**.

It also **does not establish physical causality between variables**.

ICCS helps to explore various aspects of data structure and shows which properties are preserved or changed under different stressors.

---

# Future Plans

In the next versions of the project, we plan to:

* simplify the execution of the analysis;
* add support for custom datasets;
* expand usage examples;
* further develop structural evaluation methods.
