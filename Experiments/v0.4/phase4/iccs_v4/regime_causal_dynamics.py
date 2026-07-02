import os
import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class RegimeCausalDynamics:
    """
    Module F — ICCS v0.4 Causal Regime Dynamics

    Builds:
    - directed flow field over regime manifold
    - collapse-attraction vectors
    - predictive instability scoring
    """

    def __init__(self, output_dir="causal_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load inputs
    # -----------------------------
    def load_data(self, matrix_path, curvature_path):
        matrix = pd.read_csv(matrix_path, index_col=0).values

        with open(curvature_path, "r", encoding="utf-8") as f:
            curvature_data = json.load(f)

        states = curvature_data["states"]
        curvature = np.array([
            b.get("curvature", 0.0)
            for b in curvature_data["bifurcations"]
        ])

        # fallback if no bifurcations listed
        if len(curvature) == 0:
            curvature = np.zeros(len(states))

        return matrix, states, curvature

    # -----------------------------
    # Collapse attraction field
    # -----------------------------
    def collapse_field(self, matrix, curvature):
        """
        Combine:
        - transition probability
        - curvature instability

        Produces directed "risk flow"
        """

        n = matrix.shape[0]
        field = np.zeros_like(matrix)

        curvature = curvature[:n] if len(curvature) >= n else np.pad(curvature, (0, n-len(curvature)))

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                # causal influence = flow * instability gradient
                field[i, j] = matrix[i, j] * (1.0 + curvature[j])

        # normalize
        row_sum = field.sum(axis=1, keepdims=True) + 1e-9
        field = field / row_sum

        return field

    # -----------------------------
    # Absorbing collapse prediction
    # -----------------------------
    def predict_collapse_risk(self, field, states):
        """
        Measures:
        - sink strength
        - attractor pressure
        """

        n = len(states)
        risk = {}

        for i in range(n):
            incoming = field[:, i].sum()
            outgoing = field[i, :].sum()

            sink_pressure = incoming - outgoing

            risk[str(states[i])] = float(sink_pressure)

        return risk

    # -----------------------------
    # Directed flow energy
    # -----------------------------
    def flow_energy(self, field):
        """
        Global instability energy of system
        """

        return float(np.mean(field * np.log(field + 1e-9)))

    # -----------------------------
    # Identify critical regimes
    # -----------------------------
    def critical_states(self, risk, threshold=None):
        values = np.array(list(risk.values()))

        if threshold is None:
            threshold = np.mean(values) + np.std(values)

        return [
            {"state": k, "risk": v}
            for k, v in risk.items()
            if v > threshold
        ]

    # -----------------------------
    # Visualization
    # -----------------------------
    def plot_risk(self, risk):
        plt.figure(figsize=(8, 4))

        keys = list(risk.keys())
        values = list(risk.values())

        plt.bar(keys, values)
        plt.title("ICCS v0.4 — Collapse Risk per Regime")

        out = os.path.join(self.output_dir, "collapse_risk.png")
        plt.savefig(out, dpi=300, bbox_inches="tight")
        plt.close()

        return out

    # -----------------------------
    # Full pipeline
    # -----------------------------
    def run(self, matrix_path, curvature_path):
        matrix, states, curvature = self.load_data(matrix_path, curvature_path)

        field = self.collapse_field(matrix, curvature)

        risk = self.predict_collapse_risk(field, states)
        critical = self.critical_states(risk)
        energy = self.flow_energy(field)

        plot_path = self.plot_risk(risk)

        result = {
            "states": [str(s) for s in states],
            "collapse_energy": energy,
            "risk": risk,
            "critical_states": critical,
            "plot": plot_path
        }

        out_path = os.path.join(self.output_dir, "causal_summary.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return {
            "summary": out_path,
            "plot": plot_path,
            "collapse_energy": energy,
            "critical_states": critical
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--curvature", required=True)

    args = parser.parse_args()

    engine = RegimeCausalDynamics()
    result = engine.run(args.matrix, args.curvature)

    print(json.dumps(result, indent=2))
