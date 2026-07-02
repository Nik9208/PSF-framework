import os
import json
import numpy as np
import pandas as pd

import networkx as nx
from sklearn.manifold import SpectralEmbedding
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt


class RegimeManifoldCurvature:
    """
    Module E — ICCS v0.4 Regime Manifold Curvature

    Computes:
    - latent manifold embedding of regime transitions
    - local geometric curvature approximation
    - bifurcation / instability detection
    """

    def __init__(self, output_dir="curvature_output", n_neighbors=5):
        self.output_dir = output_dir
        self.n_neighbors = n_neighbors
        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load transition matrix
    # -----------------------------
    def load_matrix(self, path: str):
        df = pd.read_csv(path, index_col=0)
        states = list(df.columns)
        matrix = df.values.astype(float)
        return matrix, states

    # -----------------------------
    # Build weighted graph
    # -----------------------------
    def build_graph(self, matrix, states):
        G = nx.DiGraph()

        for i, s_from in enumerate(states):
            for j, s_to in enumerate(states):
                w = matrix[i, j]
                if w > 0:
                    G.add_edge(s_from, s_to, weight=w)

        return G

    # -----------------------------
    # Spectral manifold embedding
    # -----------------------------
    def embed(self, matrix):
        """
        Turn transition matrix into latent geometry space
        """
        # Ensure we don't request more components than we have samples
        n_components = min(2, len(matrix))
        
        embedding = SpectralEmbedding(
            n_components=n_components,
            affinity="precomputed",
            random_state=42
        )

        coords = embedding.fit_transform(matrix)
        
        # If matrix had < 2 states, pad coords with zeros to make it 2D for plotting
        if n_components < 2:
            coords = np.pad(coords, ((0, 0), (0, 2 - n_components)), 'constant')
            
        return coords

    # -----------------------------
    # Local curvature approximation
    # -----------------------------
    def compute_curvature(self, coords, states):
        """
        Curvature proxy:
        deviation of point from local linear neighborhood
        """
        # Ensure n_neighbors is valid for the number of coordinates
        n_neighbors = min(self.n_neighbors, len(coords) - 1)
        
        if n_neighbors <= 0:
            return np.zeros(len(coords))

        nn = NearestNeighbors(n_neighbors=n_neighbors)
        nn.fit(coords)
        distances, indices = nn.kneighbors(coords)

        curvature = np.zeros(len(coords))

        for i in range(len(coords)):
            neighbors = coords[indices[i]]
            center = coords[i]

            # local centroid
            centroid = neighbors.mean(axis=0)

            # curvature proxy = deviation from local barycenter
            curvature[i] = np.linalg.norm(center - centroid)

        # normalize
        max_curv = np.max(curvature)
        if max_curv > 0:
            curvature = curvature / max_curv

        return curvature

    # -----------------------------
    # Bifurcation detection
    # -----------------------------
    def detect_bifurcations(self, curvature, states, threshold=0.7):
        """
        High curvature = structural instability
        """

        critical = []

        for i, c in enumerate(curvature):
            if c > threshold:
                critical.append({
                    "state": states[i],
                    "curvature": float(c)
                })

        return critical

    # -----------------------------
    # Global deformation score
    # -----------------------------
    def deformation_index(self, curvature):
        """
        Overall instability of manifold
        """

        return float(np.mean(curvature))

    # -----------------------------
    # Visualization
    # -----------------------------
    def plot(self, coords, curvature, states):
        plt.figure(figsize=(8, 6))

        scatter = plt.scatter(
            coords[:, 0],
            coords[:, 1],
            c=curvature,
            cmap="inferno",
            s=120,
            vmin=0,
            vmax=1.0
        )

        for i, s in enumerate(states):
            plt.text(coords[i, 0], coords[i, 1], str(s))

        plt.colorbar(scatter, label="Curvature (instability proxy)")
        plt.title("ICCS v0.4 — Regime Manifold Curvature")

        out_path = os.path.join(self.output_dir, "manifold_curvature.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()

        return out_path

    # -----------------------------
    # Full pipeline
    # -----------------------------
    def run(self, matrix_path: str):
        matrix, states = self.load_matrix(matrix_path)

        G = self.build_graph(matrix, states)
        coords = self.embed(matrix)

        curvature = self.compute_curvature(coords, states)
        bifurcations = self.detect_bifurcations(curvature, states)
        deformation = self.deformation_index(curvature)

        plot_path = self.plot(coords, curvature, states)

        result = {
            "states": states,
            "bifurcations": bifurcations,
            "deformation_index": deformation,
            "plot": plot_path
        }

        out_path = os.path.join(self.output_dir, "curvature_summary.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return {
            "summary": out_path,
            "plot": plot_path,
            "deformation_index": deformation
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    engine = RegimeManifoldCurvature()
    result = engine.run(args.input)

    print(json.dumps(result, indent=2))
