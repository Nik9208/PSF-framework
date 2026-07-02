import os
import json
import numpy as np
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt


class RegimeTransitionGraph:
    """
    Module D — ICCS v0.4 Regime Transition Graph

    Extends static regime geometry into:
    - temporal regime transitions
    - Markov transition matrix
    - directed regime graph
    - geometric stability metrics
    """

    def __init__(self, output_dir="transition_graph_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load labeled regime data
    # -----------------------------
    def load_data(self, path: str) -> pd.DataFrame:
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                df = pd.DataFrame(json.load(f))
        else:
            raise ValueError("Unsupported format")

        if "regime_cluster" not in df.columns:
            if "regime" in df.columns:
                pass
            else:
                raise ValueError("Input must contain 'regime' or 'regime_cluster' column (from Module C)")

        return df

    # -----------------------------
    # Build transition matrix
    # -----------------------------
    def compute_transitions(self, regimes: np.ndarray):
        """
        Compute empirical transition probabilities P(i -> j)
        """

        unique_states = sorted(set(regimes))
        index = {s: i for i, s in enumerate(unique_states)}

        matrix = np.zeros((len(unique_states), len(unique_states)))

        for t in range(len(regimes) - 1):
            i = index[regimes[t]]
            j = index[regimes[t + 1]]
            matrix[i, j] += 1

        # normalize rows
        row_sums = matrix.sum(axis=1, keepdims=True) + 1e-9
        matrix = matrix / row_sums

        return matrix, unique_states

    # -----------------------------
    # Build graph
    # -----------------------------
    def build_graph(self, matrix, states):
        G = nx.DiGraph()

        for i, s_from in enumerate(states):
            for j, s_to in enumerate(states):
                weight = matrix[i, j]
                if weight > 0:
                    G.add_edge(s_from, s_to, weight=weight)

        return G

    # -----------------------------
    # Stability metrics
    # -----------------------------
    def compute_stability(self, matrix, states):
        """
        Geometric stability of phase space:

        1. Diagonal dominance → stability
        2. Entropy of transitions → chaos
        3. Absorbing states → collapse regimes
        """

        diag = np.diag(matrix)
        stability_score = float(np.mean(diag))

        entropy = 0.0
        for row in matrix:
            row = row[row > 0]
            entropy -= np.sum(row * np.log(row))

        entropy /= len(states)

        # Ensure elements of states are native Python types
        states_native = [int(s) if isinstance(s, (np.int32, np.int64)) else str(s) for s in states]

        absorbing = [states_native[i] for i in range(len(states)) if matrix[i, i] > 0.85]

        return {
            "mean_self_transition": stability_score,
            "transition_entropy": float(entropy),
            "absorbing_states": absorbing
        }

    # -----------------------------
    # Visualization
    # -----------------------------
    def plot_graph(self, G, path="transition_graph.png"):
        plt.figure(figsize=(8, 6))

        pos = nx.spring_layout(G, seed=42)

        weights = [G[u][v]["weight"] for u, v in G.edges()]
        widths = [w * 5 for w in weights]

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=1500,
            node_color="lightblue",
            arrows=True,
            width=widths
        )

        plt.title("ICCS v0.4 — Regime Transition Graph")

        out_path = os.path.join(self.output_dir, path)
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()

        return out_path

    # -----------------------------
    # Full pipeline
    # -----------------------------
    def run(self, labeled_csv_path: str):
        df = self.load_data(labeled_csv_path)

        regime_col = "regime_cluster" if "regime_cluster" in df.columns else "regime"
        regimes = df[regime_col].values

        matrix, states = self.compute_transitions(regimes)
        G = self.build_graph(matrix, states)

        stability = self.compute_stability(matrix, states)
        plot_path = self.plot_graph(G)

        # Convert states to native Python types for JSON serialization
        states_native = [int(s) if isinstance(s, (np.int32, np.int64)) else str(s) for s in states]

        # save matrix
        matrix_df = pd.DataFrame(matrix, index=states_native, columns=states_native)
        matrix_path = os.path.join(self.output_dir, "transition_matrix.csv")
        matrix_df.to_csv(matrix_path)

        # save summary
        summary = {
            "states": states_native,
            "stability": stability
        }

        summary_path = os.path.join(self.output_dir, "transition_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return {
            "graph": plot_path,
            "matrix": matrix_path,
            "summary": summary_path,
            "stability": stability
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    engine = RegimeTransitionGraph()
    result = engine.run(args.input)

    print(json.dumps(result, indent=2))
