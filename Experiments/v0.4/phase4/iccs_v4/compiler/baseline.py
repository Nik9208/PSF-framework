from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


# =========================
# Utility functions
# =========================

def _rank_transform(x: np.ndarray) -> np.ndarray:
    """Map values to ranks (0..1)."""
    temp = x.argsort()
    ranks = np.empty_like(temp, dtype=float)
    ranks[temp] = np.linspace(0, 1, len(x))
    return ranks


def _match_distribution(sorted_template: np.ndarray, target: np.ndarray) -> np.ndarray:
    """
    Replace sorted values of target with sorted_template values.
    Preserves rank structure of target, enforces distribution of template.
    """
    ranks = np.argsort(np.argsort(target))
    return sorted_template[ranks]


def _spectral_error(a: np.ndarray, b: np.ndarray) -> float:
    """Relative L2 error in power spectrum."""
    pa = np.abs(np.fft.rfft(a)) ** 2
    pb = np.abs(np.fft.rfft(b)) ** 2
    return float(np.linalg.norm(pa - pb) / (np.linalg.norm(pa) + 1e-12))


# =========================
# Surrogates
# =========================

def ft_surrogate(x: np.ndarray, random_state: Optional[int] = None) -> np.ndarray:
    """
    Phase Randomization (FT surrogate).
    Preserves amplitude spectrum, destroys phase coherence.
    """
    if random_state is not None:
        np.random.seed(random_state)

    x = np.asarray(x)
    fft_vals = np.fft.rfft(x)
    amplitudes = np.abs(fft_vals)
    phases = np.angle(fft_vals)

    random_phases = np.random.uniform(0, 2 * np.pi, len(phases))
    new_fft = amplitudes * np.exp(1j * random_phases)

    return np.fft.irfft(new_fft, n=len(x))


def white_noise_surrogate(x: np.ndarray, random_state: Optional[int] = None) -> np.ndarray:
    """Gaussian white noise baseline with same mean/std."""
    if random_state is not None:
        np.random.seed(random_state)

    return np.random.normal(loc=np.mean(x), scale=np.std(x), size=len(x))


def iaaft_surrogate(
    x: np.ndarray,
    max_iter: int = 100,
    tol_spectrum: float = 1e-3,
    tol_distribution: float = 1e-3,
    random_state: Optional[int] = None,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    IAAFT surrogate generation.

    Iteratively enforces:
    - target power spectrum
    - target amplitude distribution
    """

    if random_state is not None:
        np.random.seed(random_state)

    x = np.asarray(x)
    sorted_x = np.sort(x)

    # initial condition: shuffled signal
    y = np.random.permutation(x)

    prev_spec_err = np.inf
    prev_dist_err = np.inf

    for _ in range(max_iter):
        # --- enforce spectrum ---
        fft_y = np.fft.rfft(y)
        fft_x = np.fft.rfft(x)

        phase = np.angle(fft_y)
        amp_x = np.abs(fft_x)

        y_spectral = np.fft.irfft(amp_x * np.exp(1j * phase), n=len(x))

        # --- enforce distribution ---
        y_new = _match_distribution(sorted_x, y_spectral)

        # --- diagnostics ---
        spec_err = _spectral_error(x, y_new)
        dist_err = np.mean(np.abs(np.sort(y_new) - sorted_x))

        # convergence check
        if (
            abs(prev_spec_err - spec_err) < tol_spectrum
            and abs(prev_dist_err - dist_err) < tol_distribution
        ):
            y = y_new
            break

        y = y_new
        prev_spec_err = spec_err
        prev_dist_err = dist_err

    diagnostics = {
        "spectral_error": float(prev_spec_err),
        "distribution_error": float(prev_dist_err),
        "iterations": float(_ + 1),
    }

    return y, diagnostics


# =========================
# Validation layer
# =========================

@dataclass
class BaselineDiagnostics:
    cv: float
    mean: float
    std: float
    converged: bool


def stability_conditions(x: np.ndarray, eps_conv: float = 1e-3, cv_threshold: float = 0.1) -> BaselineDiagnostics:
    """
    Baseline stability conditions:
    - CV constraint
    - simple convergence proxy (signal smoothness)
    """

    x = np.asarray(x)

    mean = np.mean(x)
    std = np.std(x)
    cv = std / (abs(mean) + 1e-12)

    # convergence proxy: local variation stability
    diffs = np.diff(x)
    conv_metric = np.mean(np.abs(diffs))

    converged = (cv < cv_threshold) and (conv_metric < eps_conv)

    return BaselineDiagnostics(
        cv=float(cv),
        mean=float(mean),
        std=float(std),
        converged=bool(converged),
    )
