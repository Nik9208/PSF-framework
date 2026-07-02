from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict


# =========================
# Utilities: entropy estimators (discrete proxy)
# =========================

def _discretize(x: np.ndarray, bins: int = 20) -> np.ndarray:
    """Discretize continuous signal into bins."""
    edges = np.histogram_bin_edges(x, bins=bins)
    return np.digitize(x, edges[:-1])


def _joint_prob(x: np.ndarray, y: np.ndarray, bins: int = 20):
    """Joint probability distribution P(X,Y)."""
    x_d = _discretize(x, bins)
    y_d = _discretize(y, bins)

    joint, _, _ = np.histogram2d(x_d, y_d, bins=bins, density=True)
    joint = joint + 1e-12
    joint = joint / np.sum(joint)
    return joint


def _entropy(p: np.ndarray) -> float:
    p = p + 1e-12
    p = p / np.sum(p)
    return float(-np.sum(p * np.log(p)))


def _conditional_entropy(joint: np.ndarray, axis: int) -> float:
    """
    H(Y|X) or H(X|Y)
    axis=0 → condition on X
    axis=1 → condition on Y
    """
    marginal = np.sum(joint, axis=axis, keepdims=True)
    cond = joint / (marginal + 1e-12)
    return _entropy(cond)


def transfer_entropy(x: np.ndarray, y: np.ndarray) -> float:
    """
    Simplified TE proxy:
    TE(X→Y) ≈ H(Y_t | Y_{t-1}) - H(Y_t | Y_{t-1}, X_{t-1})
    """

    # time shift
    x_t = x[:-1]
    y_t = y[1:]
    y_prev = y[:-1]

    # joint distributions
    j1 = _joint_prob(y_t, y_prev)
    j2 = _joint_prob(y_t + x_t, y_prev)  # proxy coupling term

    h1 = _entropy(j1)
    h2 = _entropy(j2)

    return float(h1 - h2)


# =========================
# Surrogate calibration layer
# =========================

def _calibrate(values: np.ndarray, surrogate_values: np.ndarray) -> Tuple[float, float]:
    mu = np.mean(surrogate_values)
    std = np.std(surrogate_values)
    z = (values - mu) / (std + 1e-12)
    return float(z), float(mu)


# =========================
# Output structure
# =========================

@dataclass
class TOOResult:
    te_xy: float
    te_yx: float
    asymmetry: float
    calibrated_asymmetry: float
    regime: str


# =========================
# Core TOO engine
# =========================

def too_engine(
    x: np.ndarray,
    y: np.ndarray,
    surrogate_te_xy: np.ndarray,
    surrogate_te_yx: np.ndarray,
) -> TOOResult:
    """
    TOO = Transfer Entropy Operator (directional causality layer)

    - computes TE(X→Y) and TE(Y→X)
    - removes surrogate baseline bias
    - extracts directional asymmetry
    """

    x = np.asarray(x)
    y = np.asarray(y)

    if len(x) < 5 or len(y) < 5:
        raise ValueError("Time series too short for TOO estimation")

    # =========================
    # raw transfer entropy
    # =========================
    te_xy = transfer_entropy(x, y)
    te_yx = transfer_entropy(y, x)

    # =========================
    # asymmetry signal
    # =========================
    asymmetry = te_xy - te_yx

    # =========================
    # surrogate calibration
    # =========================
    z_xy, mu_xy = _calibrate(te_xy, surrogate_te_xy)
    z_yx, mu_yx = _calibrate(te_yx, surrogate_te_yx)

    calibrated_asymmetry = z_xy - z_yx

    # =========================
    # regime classification
    # =========================
    score = abs(calibrated_asymmetry)

    if score < 0.5:
        regime = "no_directionality"
    elif score < 1.5:
        regime = "weak_flow"
    elif score < 3.0:
        regime = "structured_causality"
    else:
        regime = "dominant_directionality"

    return TOOResult(
        te_xy=float(te_xy),
        te_yx=float(te_yx),
        asymmetry=float(asymmetry),
        calibrated_asymmetry=float(calibrated_asymmetry),
        regime=regime,
    )
