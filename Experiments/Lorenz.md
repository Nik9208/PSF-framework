# Lorenz System — Representation Migration Experiment

## 1. Objective

Test whether the dominant predictive representation changes with prediction horizon.

The experiment evaluates:

$$ \Phi^*(h) = \arg\max_\Phi I(\Phi,h) $$

for different candidate representations.

---

# 2. System

The Lorenz dynamical system:

dx/dt = σ(y-x)

dy/dt = x(ρ-z)-y

dz/dt = xy-βz


Parameters:

σ = 10

ρ = 28

β = 8/3


The system demonstrates deterministic chaotic dynamics.

---

# 3. Candidate Representations

The following representations are compared:

## Local representation

Φ_local:

individual state variables:

(x)

(y)

(z)


---

## Cross-variable representation

Φ_cross:

relationships between variables:

(x,y)

(x,z)

(y,z)


---

# 4. Framework Prediction

The framework predicts:

At shorter horizons:

Φ_local may provide higher predictive accessibility.

At longer horizons:

a combined representation may become dominant.

Expected transition:

Φ_local → Φ_cross

---

# 5. Information Criterion

For each horizon h:

calculate:

$$ I(\Phi,h) $$

and compare:

$$ I(\Phi_{local},h) $$

against:

$$ I(\Phi_{cross},h) $$


The transition point occurs when:

$$ I(\Phi_{cross},h) > I(\Phi_{local},h) $$

---

# 6. Observed Result

The predictive information landscape changes with horizon.

A transition was observed:

$$ T_{transition} \approx 16 $$


Near the transition region:

$$ |G(h)| < \delta $$

indicating uncertainty between representations.

---

# 7. Interpretation

The system does not change its physical laws.

The change occurs in the optimal predictive representation.

The framework interprets this as:

Representation Migration

rather than a physical phase transition.

---

# 8. Relation to Observer Independence

Multiple models can be tested:

- Random Forest
- Neural Networks
- other predictors

The model is considered an observer.

Agreement between independent observers strengthens confidence that the transition reflects system structure.

---

# 9. Limitations

This experiment does not prove:

- causality of the selected representation;
- uniqueness of the representation;
- universal behavior for all chaotic systems.

It demonstrates horizon-dependent predictive representation change.

---

# Status

Completed validation example.

Framework component tested:

Representation Migration.
