from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple


# =========================
# Utility: distribution tools
# =========================

def _histogram_prob(x: np.ndarray, bins: int = 30) -> Tuple[np.ndarray, np.ndarray]:
    """Return normalized histogram (probability distribution)."""
    hist, bin_edges = np.histogram(x, bins=bins, density=True)
    hist = hist + 1e-12  # avoid zeros
    hist = hist / np.sum(hist)
    return hist, bin_edges


def _kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Discrete KL divergence: P || Q"""
    p = p + 1e-12
    q = q + 1e-12
    p = p / np.sum(p)
    q = q / np.sum(q)
    return float(np.sum(p * np.log(p / q)))


def _z_score(obs: float, mu: float, std: float) -> float:
    return float((obs - mu) / (std + 1e-12))


# =========================
# Core SCO engine
# =========================

@dataclass
class SCOResult:
    ft_score: float
    iaaft_score: float
    wn_score: float
    aggregate_score: float
    regime_label: str


def sco_engine(
    observed: np.ndarray,
    ft_surrogates: np.ndarray,
    iaaft_surrogates: np.ndarray,
    wn_surrogates: np.ndarray,
    bins: int = 30,
) -> SCOResult:
    """
    Surrogate Deviation Engine (SCO)

    Measures:
    - distributional separation (KL)
    - mean/variance deviation (z-score proxy)
    - regime classification
    """

    observed = np.asarray(observed)

    # =========================
    # helper stats
    # =========================
    def stats(x: np.ndarray):
        return np.mean(x), np.std(x)

    obs_mu, obs_std = stats(observed)

    # =========================
    # surrogate stats
    # =========================
    ft_mu, ft_std = stats(ft_surrogates)
    ia_mu, ia_std = stats(iaaft_surrogates)
    wn_mu, wn_std = stats(wn_surrogates)

    # =========================
    # z-score separation
    # =========================
    ft_z = abs(_z_score(obs_mu, ft_mu, ft_std))
    ia_z = abs(_z_score(obs_mu, ia_mu, ia_std))
    wn_z = abs(_z_score(obs_mu, wn_mu, wn_std))

    # =========================
    # KL divergence (distributional)
    # =========================
    obs_p, _ = _histogram_prob(observed, bins=bins)
    ft_p, _ = _histogram_prob(ft_surrogates, bins=bins)
    ia_p, _ = _histogram_prob(iaaft_surrogates, bins=bins)
    wn_p, _ = _histogram_prob(wn_surrogates, bins=bins)

    kl_ft = _kl_divergence(obs_p, ft_p)
    kl_ia = _kl_divergence(obs_p, ia_p)
    kl_wn = _kl_divergence(obs_p, wn_p)

    # =========================
    # normalized scores
    # =========================
    ft_score = ft_z + kl_ft
    iaaft_score = ia_z + kl_ia
    wn_score = wn_z + kl_wn

    aggregate = (ft_score + iaaft_score + wn_score) / 3.0

    # =========================
    # regime classification
    # =========================
    if aggregate < 0.5:
        regime = "null_like"
    elif aggregate < 1.5:
        regime = "weak_structure"
    elif aggregate < 3.0:
        regime = "structured_regime"
    else:
        regime = "strong_non_surrogate"

    return SCOResult(
        ft_score=float(ft_score),
        iaaft_score=float(iaaft_score),
        wn_score=float(wn_score),
        aggregate_score=float(aggregate),
        regime_label=regime,
    )
