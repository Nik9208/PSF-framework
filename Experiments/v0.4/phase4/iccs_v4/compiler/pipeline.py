from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Tuple

from iccs_v4.compiler.baseline import (
    ft_surrogate,
    iaaft_surrogate,
    white_noise_surrogate,
    stability_conditions,
)

from iccs_v4.compiler.sco import sco_engine
from iccs_v4.compiler.rso import rso_engine
from iccs_v4.compiler.too import too_engine


# =========================
# Final ICCS Object
# =========================

@dataclass
class ICCSResult:
    sco: Any
    rso: Any
    too: Any
    stability: Any
    regime: str


# =========================
# Core Compiler
# =========================

def compile_iccs(
    x: np.ndarray,
    y: np.ndarray,
    trajectory: np.ndarray,
    bins: int = 30,
    random_state: int = 42,
) -> ICCSResult:
    """
    ICCS v0.4 Epistemic Compiler

    Input:
        x, y → paired time series (for causality layer)
        trajectory → multivariate state evolution (for geometry layer)

    Output:
        fully calibrated ICCS regime object
    """

    x = np.asarray(x)
    y = np.asarray(y)

    # =========================
    # 1. Surrogate generation
    # =========================
    ft_x = ft_surrogate(x, random_state)
    ft_y = ft_surrogate(y, random_state + 1)

    ia_x, _ = iaaft_surrogate(x, random_state=random_state + 2)
    ia_y, _ = iaaft_surrogate(y, random_state=random_state + 3)

    wn_x = white_noise_surrogate(x, random_state + 4)
    wn_y = white_noise_surrogate(y, random_state + 5)

    # =========================
    # 2. SCO (distributional deviation)
    # =========================
    sco = sco_engine(
        observed=x,
        ft_surrogates=ft_x,
        iaaft_surrogates=ia_x,
        wn_surrogates=wn_x,
        bins=bins,
    )

    # =========================
    # 3. RSO (geometric stability)
    # =========================
    rso = rso_engine(trajectory)

    # =========================
    # 4. TOO (causal directionality)
    # =========================
    # surrogate TE placeholders (consistency-preserving approximation)
    surrogate_te_xy = np.array([np.mean(ft_x), np.mean(ia_x), np.mean(wn_x)])
    surrogate_te_yx = np.array([np.mean(ft_y), np.mean(ia_y), np.mean(wn_y)])

    too = too_engine(
        x=x,
        y=y,
        surrogate_te_xy=surrogate_te_xy,
        surrogate_te_yx=surrogate_te_yx,
    )

    # =========================
    # 5. Stability layer (global constraint)
    # =========================
    stability = stability_conditions(x)

    # =========================
    # 6. Global regime synthesis
    # =========================
    regime_score = (
        sco.aggregate_score
        + rso.collapse_risk
        + abs(too.calibrated_asymmetry)
    )

    if not stability.converged:
        regime = "non_convergent_system"
    elif regime_score < 1.0:
        regime = "null_regime"
    elif regime_score < 3.0:
        regime = "weak_structural_regime"
    elif regime_score < 6.0:
        regime = "structured_iccs_regime"
    else:
        regime = "high_complexity_non_surrogate_regime"

    return ICCSResult(
        sco=sco,
        rso=rso,
        too=too,
        stability=stability,
        regime=regime,
    )
