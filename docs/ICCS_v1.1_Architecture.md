# ICCS v1.1 Architecture

## Feature Space

$S(X) = [M(k), D_{local}, TE_{forward}, TE_{reverse}, CMI]$

## Components

### Dynamics Layer

Measures:
- multi-step predictive memory
- temporal organization

Component:
$M(k)$

---

### Geometry Layer

Measures:
- intrinsic state-space structure
- representation robustness

Component:
$D_{local}$

---

### Causal Layer

Measures:
- directional information flow
- conditional independence

Components:
$TE_{+}, TE_{-}, CMI$

---

## Aggregation Principle

ICCS v1.1 should not collapse all dimensions prematurely.

The scalar score must preserve:

1. dynamics information
2. geometric invariants
3. causal asymmetry

Validation requirement:

Two systems with different structural fingerprints must not become identical after aggregation.
