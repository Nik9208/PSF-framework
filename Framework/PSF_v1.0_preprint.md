# Operational Framework v1.0-preprint

## Predictive Representation Analysis in Dynamical Systems

### Status

Research framework under validation.

This document defines an operational approach for identifying predictive structures in dynamical systems and separating system-dependent predictive information from observer-induced representations.

---

# Abstract

A dynamical system does not necessarily possess a single fixed predictive representation.

Instead, predictive structure may depend on:

- prediction horizon,
- available information,
- representation space,
- observer constraints.

The framework defines an optimal predictive representation as the representation that maximizes accessible predictive information under a temporal constraint:

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

where:
- $\Phi$ — candidate representation,
- $h$ — prediction horizon,
- $I(\Phi,h)$ — predictive information available in representation $\Phi$.

Machine learning models are treated as observers and measurement instruments rather than sources of physical structure.

---

# 1. Core Principle

The central hypothesis:

A predictive structure is not defined as a fixed variable of a dynamical system.

It is defined as a representation that provides maximal stable predictive accessibility for a given prediction horizon.

Therefore, different horizons may produce different optimal representations.

---

# 2. Predictive Representation

For a dynamical system $X(t)$, a set of candidate representations is considered:

$$ \Phi = \{\Phi_1, \Phi_2, ..., \Phi_n\} $$

For each representation, $I(\Phi,h)$ measures the amount of information available for prediction over horizon $h$.

The optimal representation:

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

---

# 3. Representation Regimes

## Regime I — Representation Migration

Condition:

$$ I(\Phi_B,h) > I(\Phi_A,h) $$

and the dominant predictive domain changes.

Examples:
- **Lorenz**: local variables $\rightarrow$ cross-variable representation
- **Rössler**: coordinate representation $\rightarrow$ phase representation
- **Fisher-KPP**: temporal representation $\rightarrow$ spatial representation

---

## Regime II — Representation Refinement

The predictive domain remains unchanged:

$$ \text{Domain}(\Phi_A) = \text{Domain}(\Phi_B) $$

but the mathematical description improves.

Example:
- **Logistic Map**: linear description $\rightarrow$ nonlinear representation

---

## Regime III — Information Horizon Collapse

Condition:

$$ \max_\Phi I(\Phi,h) < \epsilon $$

Predictive structure becomes inaccessible at the chosen horizon.

Examples:
- high horizon chaotic prediction
- high-noise stochastic systems

---

# 4. Observer Independence Principle

Machine learning models do not reveal physical structure directly.

A model may select a representation because of:
- algorithmic bias,
- architecture,
- feature preference.

Therefore:
**model importance $\neq$ physical predictive structure.**

The framework separates physical predictive accessibility from observer-induced representation preference.

---

# 5. Observer-Induced Migration (Regime IV)

A false migration can occur when:

$$ I(\Phi_A,h) > I(\Phi_B,h) $$

but:

$$ Importance_{obs}(\Phi_B) > Importance_{obs}(\Phi_A) $$

The observer selects a convenient representation rather than the most physically predictive one.

---

# 6. Information Conditioned Carrier Score (ICCS)

To distinguish predictive structure from observer effects:

$$ ICCS(\Phi,h) = PIS(\Phi,h) \times AO(\Phi,h) $$

where:
- **PIS** (Predictive Information Share): $\frac{I(\Phi,h)}{\sum I(\Phi_j,h)}$
- **AO** (Algorithmic Observability): $\frac{Imp_{obs}(\Phi,h)}{\max Imp_{obs}(\Phi_j,h)}$

Higher ICCS indicates stronger agreement between predictive accessibility and observer selection.

---

# 7. Experimental Validation

The framework was evaluated on:
- Lorenz system
- Rössler system
- Logistic map
- Van der Pol oscillator
- Duffing oscillator

Observed behaviors:
- **Lorenz**: consistent representation migration.
- **Rössler**: phase representation became dominant at longer horizons.
- **Van der Pol**: observer-dependent false migration detected.
- **Logistic map**: nonlinear refinement preserved predictive structure.
- **Duffing**: chaotic and noise-induced collapse distinguished.

---

# 8. Limitations

The framework does not claim:
- mutual information equals causality;
- predictive representation equals physical mechanism;
- machine learning discovers fundamental laws;
- all hidden variables are observable.

Predictive accessibility is not identical to causal explanation.

---

# 9. Future Work

Boundary stress tests (Project X):
- hidden variable systems;
- causal/predictive divergence;
- adversarial representations;
- equal-information representations;
- observer robustness testing.

---

# Conclusion

The framework proposes an operational definition of predictive structure.

Structure is treated as an accessible predictive property under temporal constraints rather than a single fixed mathematical object.

The goal is not to replace physical theory, but to provide a method for analyzing how predictive structure appears, changes, and becomes inaccessible in dynamical systems.
