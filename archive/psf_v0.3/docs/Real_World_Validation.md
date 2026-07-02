## Real-World Validation Protocol (C-MAPSS)

### Epistemological Goal

The objective of this real-world validation on the NASA C-MAPSS dataset is not to develop a state-of-the-art Predictive Maintenance (RUL prediction) model.

Instead, we evaluate whether the ICCS structural representation remains informative under real-world temporal degradation, representation compression, and observational noise.

### Main Hypothesis

The multidimensional ICCS profile:

$S(X) = [M(k), D_{local}, TE_{forward}, TE_{reverse}, CMI]$

preserves structural transitions better than scalar health indicators under boundary perturbations.

We hypothesize that multivariate dependency structures between engine channels change during degradation, and that different ICCS components exhibit different robustness profiles.

---

## Evaluation Suite

### Experiment 1: Temporal Boundary

**Objective**:
Track evolution of structural complexity during degradation.

**Method**:
- Select engine trajectories from FD001.
- Partition trajectories into:
  - Early degradation
  - Intermediate degradation
  - Late degradation
- Compute ICCS profiles over temporal windows.
- Compare component trajectories.

**Expected outcome**:
Identify whether different structural properties degrade at different stages.

---

### Experiment 2: Representation Boundary

**Objective**:
Measure structural information loss under representation changes.

**Representations**:
1. Raw sensor trajectories
2. Statistical feature representation
3. PCA reduced representation
4. Scalar health indicator

**Evaluate**:
- ICCS preservation
- structural separation
- information collapse

**Expected outcome**:
Determine which representations preserve multivariate dependency structure.

---

### Experiment 3: Noise Boundary

**Objective**:
Evaluate robustness under observational uncertainty.

**Noise levels**:
0%, 5%, 10%, 20%

**Measure**:
- ICCS component degradation
- failure regime transitions
- comparison against scalar baselines

**Expected outcome**:
Validate whether robustness patterns observed in synthetic systems generalize to real sensor data.
