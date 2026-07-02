import os
import json
import numpy as np
import pandas as pd


class RegimeControlLayer:
    """
    Module G — ICCS v0.4 Control Layer (Anti-Collapse Policy Synthesis)

    Goal:
    - modify transition dynamics in latent regime space
    - reduce probability of collapse / sink states
    - stabilize high-curvature bifurcation zones
    """

    def __init__(self, alpha=0.3, beta=0.7, output_dir="control_output"):
        """
        alpha -> strength of intervention
        beta  -> weight of risk suppression
        """
        self.alpha = alpha
        self.beta = beta
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load inputs
    # -----------------------------
    def load_inputs(self, matrix_path, risk_path):
        matrix = pd.read_csv(matrix_path, index_col=0).values

        with open(risk_path, "r", encoding="utf-8") as f:
            risk_data = json.load(f)

        states = list(risk_data["states"])
        risk_map = risk_data["risk"]

        risk = np.array([risk_map[str(s)] for s in states])

        return matrix, states, risk

    # -----------------------------
    # Compute intervention field
    # -----------------------------
    def intervention_field(self, matrix, risk):
        """
        We penalize transitions toward high-risk states
        and reinforce stable states.
        """

        n = matrix.shape[0]
        adjusted = matrix.copy()

        risk_range = np.max(risk) - np.min(risk)
        if risk_range > 0:
            risk = (risk - np.min(risk)) / (risk_range + 1e-9)
        else:
            risk = np.zeros_like(risk)

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                # suppression of high-risk targets
                risk_penalty = 1.0 - self.beta * risk[j]

                adjusted[i, j] *= (1.0 - self.alpha + self.alpha * risk_penalty)

        # renormalize
        row_sum = adjusted.sum(axis=1, keepdims=True) + 1e-9
        adjusted = adjusted / row_sum

        return adjusted

    # -----------------------------
    # Stability gain metric
    # -----------------------------
    def stability_gain(self, original, controlled):
        """
        Measures how much we reduced "chaotic flow"
        """

        orig_entropy = -np.sum(original * np.log(original + 1e-9))
        ctrl_entropy = -np.sum(controlled * np.log(controlled + 1e-9))

        return float(orig_entropy - ctrl_entropy)

    # -----------------------------
    # Detect control bias
    # -----------------------------
    def control_shift(self, original, controlled):
        """
        Measures how much structure we distorted
        """

        return float(np.linalg.norm(original - controlled))

    # -----------------------------
    # Main pipeline
    # -----------------------------
    def run(self, matrix_path, risk_path):
        matrix, states, risk = self.load_inputs(matrix_path, risk_path)

        controlled = self.intervention_field(matrix, risk)

        gain = self.stability_gain(matrix, controlled)
        shift = self.control_shift(matrix, controlled)

        result = {
            "states": states,
            "stability_gain": gain,
            "control_shift": shift,
            "controlled_matrix": controlled.tolist()
        }

        out_path = os.path.join(self.output_dir, "control_summary.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return {
            "summary": out_path,
            "stability_gain": gain,
            "control_shift": shift
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--risk", required=True)

    args = parser.parse_args()

    engine = RegimeControlLayer()
    result = engine.run(args.matrix, args.risk)

    print(json.dumps(result, indent=2))
