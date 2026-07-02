# Causal-aware Result v0.1

## Candidate

Causal Fingerprint

$C(X,Y) = [TE_{X\rightarrow Y}, TE_{Y\rightarrow X}, CMI]$

## Motivation

Boundary Validation #3 showed:

$Prediction \neq Causation$

Predictive information and stability alone cannot distinguish:

* direct causal influence
* hidden common drivers
* reverse causality
* predictive temporal mimicry

## Experiment

Systems tested:

| System | Structure                   |
| ------ | --------------------------- |
| A      | Direct causation: X → Y     |
| B      | Common driver: Z → X, Z → Y |
| C      | Reverse causation: Y → X    |
| D      | Predictive mimic            |

All systems were matched by predictive information:

$MI(X_t;Y_{t+1}) \approx 0.30$

## Results

| System | TE X→Y | TE Y→X |    CMI |
| ------ | -----: | -----: | -----: |
| A      | 0.2432 | 0.0000 | 0.0678 |
| B      | 0.0028 | 0.0140 | 0.0000 |
| C      | 0.0136 | 0.2272 | 0.0459 |
| D      | 0.0047 | 0.0339 | 0.2883 |

## Interpretation

The causal fingerprint separates tested system classes under this experimental design.

Observed:

* Direct causation produces directional TE asymmetry.
* Reverse causation produces inverted asymmetry.
* Common-driver systems lose directional transfer after conditioning.
* Predictive mimic systems retain prediction but show no causal transfer.

## Conclusion

Causal Fingerprint is accepted as:

Causal-aware candidate v0.1.

Limitations:

* TE and CMI currently use residual-based approximations.
* Results assume approximately linear conditional structure.
* Nonlinear causal mechanisms require further validation.

## ICCS v1.1 Feature Vector

Current validated feature space:

$S(X)= [M(k), D_{local}, TE_{+}, TE_{-}, CMI]$

Next phase:

Construct ICCS v1.1 aggregation layer without collapsing independent structural dimensions.
