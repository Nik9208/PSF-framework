# Phase 3: Cross-Domain Validation Protocol

## 1. Goal Description
Phase 3 evaluates the applicability conditions of the frozen ICCS v0.3.1 reference implementation across heterogeneous real-world domains. The objective is not to demonstrate universal utility, but to identify the conditions under which the framework produces reproducible and interpretable representations, and document situations in which the resulting profiles require additional methodological caution.

**Success is not required**
Scientific validity does not depend on positive findings. Phase 3 is considered successful if it accurately characterizes the operational behavior of ICCS v0.3.1 under the predefined protocol, regardless of whether the observed results support or challenge the expected applicability of the framework.

**Scope**
Phase 3 is an observational validation study. It is not intended to optimize ICCS parameters, compare ICCS against competing methods, or establish causal relationships within the investigated domains. The objective is to characterize the behavior and applicability boundaries of the frozen reference implementation under real-world conditions.

**Out-of-Scope**
Phase 3 is explicitly NOT designed for:
- Parameter optimization or tuning of ICCS
- Searching for the "best" preprocessing methods
- Data dredging (e.g., cherry-picking "clean" segments of signals)
- Model fitting or supervised learning

*Phase 3 contains no model fitting, parameter optimization, or supervised learning. The objective is observational validation of the frozen ICCS v0.3.1 implementation.*

This phase strictly adheres to the **BVP Golden Rule**, newly established as a permanent foundational principle of the ICCS project:
> **No modification of the reference implementation is introduced on the basis of improved benchmark performance alone. Any methodological change must first demonstrate that it preserves or improves the semantic interpretability of the measured quantities under the Boundary Validation Protocol.**

**Primary endpoint:** Determine whether ICCS v0.3.1 produces reproducible and domain-interpretable profiles under realistic data conditions while being interpreted in the context of the operational boundaries established in Phase 1 and Phase 2A.

## 2. Prior knowledge carried into Phase 3
Interpretation of Phase 3 results shall explicitly account for the experimentally established limitations:
- Geometry may become unstable on strictly periodic low-dimensional signals.
- Geometry operates on scalar projections only.
- Delay embedding is intentionally excluded from the reference implementation.
- Memory and Transfer Entropy are interpreted independently of Geometry.

## 3. Research Questions
Phase 3 is designed to answer four specific research questions rather than to prove general validity:
1. **RQ1:** Does ICCS produce reproducible profiles within a single domain? *(Reproducibility will be assessed across repeated analyses using identical preprocessing pipelines and, where stochastic procedures are involved, multiple random seeds.)*
2. **RQ2:** Do similar dynamical regimes produce similar ICCS profiles across domains?
3. **RQ3:** Which components (Geometry, Memory, Transfer) remain stable under realistic noise, missing data, and preprocessing choices?
4. **RQ4:** Which observed profile differences can plausibly be attributed to domain-specific dynamics, and which are better explained by known properties of the individual ICCS components?

**The research questions are frozen prior to analysis. Additional questions arising during the study will be documented separately as exploratory analyses and will not modify the predefined objectives of Phase 3.**

## 4. Domain Selection Strategy
Domains are selected specifically because they represent different classes of real-world dynamical systems, not merely for popularity:

| Domain | Recommended dataset | Rationale for Inclusion |
| :--- | :--- | :--- |
| **Physiology** | **PhysioNet Normal Sinus Rhythm Database (NSRDB)** | Healthy subjects, high recording quality, widely used in HRV research, minimizes pathology effects on initial validation. |
| **Climate** | **NOAA Niño 3.4 SST Index** | Highly studied climate index, pronounced long-term variability, vast literature for interpretation. |
| **Economics** | **S&P 500 Daily Index (Log Returns)** | Log returns are closer to stationarity compared to raw prices. Preserves reproducibility via static CSV files. |

## 5. Dataset Registry Requirement
Every dataset analyzed must be documented in `registry/dataset_registry.md` with the following mandatory fields prior to analysis:
- Dataset name
- Version
- Source
- Download date
- License
- Citation
- SHA256 checksum (raw file)
- SHA256 checksum (preprocessed file)
- Exact number of observations
- Processing script version

## 6. Data Quality Criteria
Before analysis, each dataset must pass a documented quality check to separate algorithmic limitations from data artifacts:

| Criterion | Recorded |
| :--- | :--- |
| Completeness | [ ] |
| Missing value fraction | [ ] |
| Sampling frequency | [ ] |
| Time span covered | [ ] |
| Units of measurement | [ ] |
| Preprocessing log | [ ] |
| Effective sample length | [ ] |
| Assumptions relevant to the applied ICCS components | [ ] |

## 7. Analytical Principles
To prevent algorithmic over-interpretation, Phase 3 mandates the following principles:

1. **Domain-first interpretation:** Establish what is already known by domain experts about the specific dataset, compute the unadjusted ICCS v0.3.1 profile, and evaluate whether the metric maps meaningfully onto the domain reality. Domain knowledge provides contextual interpretation but is not treated as ground truth for validating ICCS outputs.
2. **Analysis Freeze:** Once preprocessing has been completed and the ICCS analysis has started for a given dataset, no preprocessing or parameter modifications will be introduced for that dataset. Any subsequent changes require a new documented analysis.
3. **Dataset Freeze:** All subsequent ICCS analyses MUST use the frozen preprocessed dataset. Any modification of preprocessing requires creation of a new dataset version and a new registry entry.
4. **Cross-domain comparability:** Cross-domain comparisons will be interpreted qualitatively unless differences in sampling characteristics and preprocessing are explicitly accounted for.
5. **Conditional Surrogate Testing:** Surrogate testing (e.g., IAAFT, phase-randomization) is required for domains where temporal dependence or spectral structure may confound causal or memory-based ICCS components. All surrogate comparisons in non-stationary domains (e.g., Economics) are interpreted conditionally on volatility regime preservation loss.

## 8. Preliminary Interpretation Criteria
To avoid post-hoc justification, outcomes will be categorized according to the following predefined criteria:

| Outcome | Interpretation |
| :--- | :--- |
| **Expected** | Is consistent with current expectations regarding ICCS behavior. |
| **Unexpected but reproducible** | Requires further methodological or domain investigation. |
| **Unstable** | Handled as a methodological boundary/limitation of the method. |

## 9. Exploratory Analyses
Any analyses not directly addressing RQ1–RQ4 will be explicitly labeled as exploratory and will not be used to justify methodological changes without independent validation.

## 10. Negative Outcomes
The following outcomes are considered scientifically informative:
- Failure of profile reproducibility
- Inconsistent behavior across domains
- Domain-dependent instability
- Inability to assign interpretable meaning to one or more ICCS components

Negative findings will be documented as operational boundaries rather than treated as project failures.

## 11. Execution Roadmap & Deliverables
To ensure pipeline stability, Phase 3 is executed iteratively, establishing a complete trace for each domain before proceeding to the next.

### Roadmap
- **Step 3.0: Dataset Registry** (Establish `registry/dataset_registry.md` and `environment.md`)
- **Step 3.1A: Pilot Domain (Physiology)** 
  - Complete end-to-end pipeline validation on PhysioNet NSRDB.
- **Step 3.1B: Climate Domain** (Connect NOAA data if Pilot is stable)
- **Step 3.1C: Economics Domain** (Connect static S&P500 data)
- **Step 3.2: Cross-Domain Synthesis** (Evaluation against RQ1-RQ4)

### Deliverables
Upon completion of Phase 3, the following artifacts must be present in the designated directory structure:
- `registry/dataset_registry.md`
- `registry/environment.md`
- `[domain]/integrity_report.md` (per domain)
- `[domain]/preprocessing_log.md` (per domain)
- `[domain]/iccs_results.csv` (per domain)
- `[domain]/domain_report.md` (per domain)
- `[domain]/decision_record.md` (domain-specific decision records)
- `synthesis/Phase3_Decision_Record.md`
- `synthesis/Research_Synthesis_v0.5.md`

### Phase 3 Completion Criteria
Phase 3 will be considered complete when:
1. All selected domains have been analyzed.
2. RQ1–RQ4 have been explicitly answered.
3. Domain-specific Decision Records have been produced.
4. A Phase 3 Cross-Domain Decision Record has been produced.
5. The operational boundaries observed in real-world data have been integrated into the ICCS methodology.
6. All deviations from the protocol, if any, have been explicitly documented.
7. All deliverables have been generated.
8. All interpretations are explicitly linked either to observed evidence, prior knowledge, or identified uncertainties.
