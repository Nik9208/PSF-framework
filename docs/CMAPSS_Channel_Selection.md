# C-MAPSS Channel Selection Protocol (Phase 0)

## Rationale

To ensure the purity of the ICCS validation experiments on the C-MAPSS dataset, we avoid selecting sensors based on degradation strength, failure proximity, or expected experimental outcome.

Optimizing input channels according to the desired result introduces selection bias and violates the Boundary Validation Protocol (BVP).

Therefore, channel selection (Phase 0) is performed **before any ICCS degradation analysis**. The objective is to remove uninformative channels, reduce redundancy, and construct a structurally diverse multivariate basis ($X, Y, Z$).

## Protocol Steps

### 1. Variance Filtering

**Condition:**
Sensors with zero or near-zero variance across trajectories are discarded.

**Justification:**
Flat sensors provide insufficient dynamic information and cannot contribute meaningful information transfer or local geometric structure.

---

### 2. Redundancy Reduction

**Condition:**
Remaining sensors are grouped using Mutual Information (MI) or rank correlation clustering.

The clustering procedure does not use degradation labels, RUL values, or failure proximity information.

**Justification:**
Highly redundant sensors measuring coupled physical processes may artificially inflate dependency estimates and reduce the effective dimensionality of the local state space.

---

### 3. Physical Cluster Selection

**Condition:**
Representative sensors are selected from distinct clusters to form the ICCS input basis.

Selection criteria:

* Non-zero variance
* Low intra-cluster redundancy
* High inter-cluster separation
* Physical interpretability

**Justification:**
This ensures that ICCS measures interactions between structurally distinct signal sources rather than duplicated measurements.

## Output

The protocol produces a static configuration file:

`selected_channels.yaml`

All subsequent ICCS experiments:

* Temporal Boundary
* Representation Boundary
* Noise Boundary

strictly read from this configuration to maintain a fixed unbiased baseline.

## Interpretation Note

Within the C-MAPSS validation context, Transfer Entropy (TE) and Conditional Mutual Information (CMI) are interpreted as measures of **directed dependency structure** between sensor subsystems, not as direct measurements of physical causality.
