from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple


# =========================
# Utilities: geometric proxies
# =========================

def _finite_diff(x: np.ndarray) -> np.ndarray:
    return np.diff(x, axis=0)


def _l2_norm(x: np.ndarray) -> float:
    return float(np.sqrt(np.sum(x ** 2)))


def _rowwise_norms(x: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum(x ** 2, axis=1))


# =========================
# RSO Output
# =========================

@dataclass
class RSOResult:
    stability_index: float
    drift: float
    curvature: float
    sensitivity: float
    collapse_risk: float
    regime: str


# =========================
# Core RSO Engine
# =========================

def rso_engine(trajectory: np.ndarray) -> RSOResult:
    """
    RSO = Regime Stability Operator

    Input:
        trajectory: shape (T, D)
            time-ordered ICCS state vectors or metric embeddings

    Output:
        geometric stability diagnostics
    """

    traj = np.asarray(trajectory)

    if len(traj) < 3:
        raise ValueError("Trajectory must have at least 3 time steps")

    # =========================
    # 1. Drift (first-order dynamics)
    # =========================
    d1 = _finite_diff(traj)
    drift_vec = np.mean(np.abs(d1), axis=0)
    drift = _l2_norm(drift_vec)

    # =========================
    # 2. Curvature (second-order dynamics)
    # =========================
    d2 = _finite_diff(d1)
    curvature_vec = np.mean(np.abs(d2), axis=0)
    curvature = _l2_norm(curvature_vec)

    # =========================
    # 3. Sensitivity (local volatility)
    # =========================
    local_norms = _rowwise_norms(d1)
    sensitivity = float(np.std(local_norms) / (np.mean(local_norms) + 1e-12))

    # =========================
    # 4. Stability index (inverse energy growth)
    # =========================
    energy = np.mean(local_norms)
    stability_index = 1.0 / (energy + curvature + 1e-12)

    # =========================
    # 5. Collapse risk (nonlinear instability proxy)
    # =========================
    collapse_risk = (drift * curvature) * (1.0 + sensitivity)

    # =========================
    # 6. Regime classification
    # =========================
    if collapse_risk < 0.1:
        regime = "stable_manifold"
    elif collapse_risk < 0.5:
        regime = "weak_instability"
    elif collapse_risk < 1.5:
        regime = "transition_zone"
    else:
        regime = "collapse_prone"

    return RSOResult(
        stability_index=float(stability_index),
        drift=float(drift),
        curvature=float(curvature),
        sensitivity=float(sensitivity),
        collapse_risk=float(collapse_risk),
        regime=regime,
    )
