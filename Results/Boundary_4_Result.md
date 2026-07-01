# Boundary Test #4: Aggregation Collapse Result

## Objective

Determine whether the multidimensional structural feature space $S(X) = [M, D_{local}, TE_{+}, TE_{-}, CMI]$ can be collapsed into a scalar ICCS score without losing critical structural distinctions.

## Hypothesis

A candidate aggregation should preserve separation between structurally distinct systems.
$S(A) \not\sim S(B) \implies ICCS(A) \not\approx ICCS(B)$

## Experiment

Systems tested (represented by their empirical structural profiles):

*   **System A (Predictive Mimic):** High prediction, low geometry, no causality.
*   **System B (Direct Causal):** Moderate prediction, moderate geometry, strict causality.
*   **System C (Complex Geometry):** Low prediction, high geometric complexity, no causality.

Aggregation methods evaluated:

1.  **Linear Sum** (Feature Compensation vulnerability)
2.  **Multiplicative** (Logical AND penalization)
3.  **Structural Distance** (Distance to Ideal Causal System)
4.  **Pareto Rank** (Partial ordering)

## Results

| Aggregation Method | Result | Failure Mode / Observation |
| :--- | :--- | :--- |
| **Linear** | **FAIL** | Feature compensation. $ICCS(A) \approx ICCS(B)$. A mimic with no causality scored exactly the same as a genuine causal system due to overpowering predictability. |
| **Multiplicative** | **FAIL** | Over-penalization. Complex geometry system $C$ received a score of $0$ because it lacked directional causal transfer, completely ignoring its topological richness. |
| **Structural Distance**| **PARTIAL** | Preserves structure but imposes arbitrary value judgments depending on where the "target" system is placed in the vector space. |
| **Pareto Rank** | **PASS** | Revealed that Systems A, B, and C are all Pareto-optimal. None strictly dominates another across all dimensions. |

## Interpretation

The empirical data firmly proves that complex system structure is an inherently multidimensional property.

Attempting to force distinct physical realities (memory, topology, causal flow) into a single scalar score leads directly to **Aggregation Collapse**. Different systems achieve the same scalar score through completely different, non-fungible mechanisms.

## Conclusion

**Within the PSF validation framework, the validated structural descriptors behave as independent dimensions that are not preserved by the tested scalar aggregation schemes.** 

Consequently, the primary ICCS v1.1 representation is the structural feature vector rather than a single scalar score:
$S(X) = [M(k), D_{local}, TE_{+}, TE_{-}, CMI]$

Any scalar ICCS summary may be useful for heuristic ranking or visualization, but must be accompanied by the Pareto rank and the full vector representation to prevent structural collapse.
