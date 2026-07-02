from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, List

import json
from iccs_v4.compiler.pipeline import compile_iccs
from iccs_v4.regime_geometry import RegimeGeometry
from iccs_v4.regime_transition_graph import RegimeTransitionGraph
from iccs_v4.regime_manifold_curvature import RegimeManifoldCurvature
from iccs_v4.regime_causal_dynamics import RegimeCausalDynamics
from iccs_v4.regime_control_layer import RegimeControlLayer
from iccs_v4.regime_self_optimizing_compiler import SelfOptimizingRegimeCompiler


# =========================
# Benchmark container
# =========================

@dataclass
class BenchmarkResult:
    name: str
    regime: str
    sco_score: float
    rso_risk: float
    too_asymmetry: float


# =========================
# Synthetic systems
# =========================

def stable_system(T: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Coupled AR(1)-like stable system
    """
    x = np.zeros(T)
    y = np.zeros(T)

    noise = np.random.normal(0, 0.1, T)

    for t in range(1, T):
        x[t] = 0.7 * x[t - 1] + noise[t]
        y[t] = 0.6 * y[t - 1] + 0.2 * x[t - 1] + noise[t] * 0.5

    x += 5.0
    y += 5.0
    trajectory = np.stack([x, y], axis=1)
    return x, y, trajectory


def chaotic_system(T: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Logistic-map driven coupled chaos
    """
    x = np.zeros(T)
    y = np.zeros(T)

    x[0], y[0] = 0.2, 0.7

    for t in range(T - 1):
        x[t + 1] = 4.0 * x[t] * (1 - x[t])
        y_next = 3.9 * y[t] * (1 - y[t])
        y[t + 1] = (1 - 0.05) * y_next + 0.05 * x[t + 1]

    x += 5.0
    y += 5.0
    trajectory = np.stack([x, y], axis=1)
    return x, y, trajectory


def degenerate_system(T: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Quantized sine collapse (Phase 3 failure mode analog)
    """
    t = np.linspace(0, 20, T)

    x = np.sin(t)
    y = np.sin(t + 0.1)

    # quantization collapse
    x = np.round(x * 3) / 3
    y = np.round(y * 3) / 3
    
    x += 5.0
    y += 5.0

    trajectory = np.stack([x, y], axis=1)
    return x, y, trajectory


# =========================
# Runner
# =========================

def run_benchmark() -> List[BenchmarkResult]:
    tests = {
        "stable_system": stable_system,
        "chaotic_system": chaotic_system,
        "degenerate_system": degenerate_system,
    }

    results = []
    
    # Generate 10 iterations per system to create a dataset for clustering
    for i in range(10):
        for name, generator in tests.items():
            # Seed the random number generator implicitly via pipeline's random_state
            x, y, traj = generator()
            iccs = compile_iccs(x, y, traj, random_state=i*100)

            result = BenchmarkResult(
                name=name,
                regime=iccs.regime,
                sco_score=iccs.sco.aggregate_score,
                rso_risk=iccs.rso.collapse_risk,
                too_asymmetry=iccs.too.calibrated_asymmetry,
            )
            results.append(result)
            print(f"Iter {i} | {name}: SCO={result.sco_score:.2f}, RSO={result.rso_risk:.2f}, TOO={result.too_asymmetry:.2f}")

    # Dump to JSON
    json_path = "benchmark_output.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([vars(r) for r in results], f, indent=2)

    print(f"\n[+] Saved {len(results)} samples to {json_path}")
    
    # Run Module C
    print("\n[+] Running Module C: Regime Geometry Reconstruction...")
    rg = RegimeGeometry(n_clusters=3)
    rg_result = rg.run(json_path)
    print(json.dumps(rg_result, indent=2))

    # Run Module D
    print("\n[+] Running Module D: Regime Transition Graph...")
    tg = RegimeTransitionGraph()
    tg_result = tg.run(rg_result["csv"])
    print(json.dumps(tg_result, indent=2))

    # Run Module E
    print("\n[+] Running Module E: Regime Manifold Curvature...")
    cm = RegimeManifoldCurvature()
    cm_result = cm.run(tg_result["matrix"])
    print(json.dumps(cm_result, indent=2))

    # Run Module F
    print("\n[+] Running Module F: Causal Regime Dynamics...")
    cd = RegimeCausalDynamics()
    cd_result = cd.run(
        tg_result["matrix"],
        cm_result["summary"]
    )
    print(json.dumps(cd_result, indent=2))

    # Run Module G
    print("\n[+] Running Module G: Anti-Collapse Policy Synthesis...")
    ctrl = RegimeControlLayer(alpha=0.4, beta=0.8)
    ctrl_result = ctrl.run(
        tg_result["matrix"],
        cd_result["summary"]
    )
    print(json.dumps(ctrl_result, indent=2))

    # Run Module H
    print("\n[+] Running Module H: Self-Optimizing Regime Compiler...")
    compiler = SelfOptimizingRegimeCompiler()
    compiler_result = compiler.run(json_path)
    print(json.dumps(compiler_result, indent=2))

    return results

    pass


# =========================
# Optional execution entry
# =========================

if __name__ == "__main__":
    run_benchmark()
