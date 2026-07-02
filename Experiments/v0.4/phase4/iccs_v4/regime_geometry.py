import os
import json
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


class RegimeGeometry:
    """
    Module C — ICCS v0.4 Regime Geometry Reconstruction

    Converts benchmark outputs into:
    - normalized feature space
    - reduced phase space (PCA)
    - clustering (KMeans)
    - 3D regime geometry visualization
    """

    def __init__(self, n_clusters=3, output_dir="regime_geometry_output"):
        self.n_clusters = n_clusters
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

        self.scaler = StandardScaler()
        self.pca = PCA(n_components=3)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)

    # -----------------------------
    # Load benchmark output
    # -----------------------------
    def load_benchmark(self, path: str) -> pd.DataFrame:
        """
        Expected format: JSON or CSV from benchmark_runner.py
        Must contain numeric columns representing metrics.
        """

        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            df = pd.DataFrame(data)

        elif path.endswith(".csv"):
            df = pd.read_csv(path)

        else:
            raise ValueError("Unsupported file format: use .json or .csv")

        return df

    # -----------------------------
    # Feature extraction
    # -----------------------------
    def build_feature_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Keeps only numeric columns and removes NaNs.
        """

        numeric_df = df.select_dtypes(include=[np.number]).copy()
        numeric_df = numeric_df.dropna(axis=0)

        if numeric_df.shape[1] < 3:
            raise ValueError("Need at least 3 numeric features for geometry reconstruction")

        return numeric_df

    # -----------------------------
    # Fit pipeline
    # -----------------------------
    def fit(self, X: pd.DataFrame):
        """
        Full pipeline:
        scaling -> PCA -> clustering
        """

        X_scaled = self.scaler.fit_transform(X)
        X_pca = self.pca.fit_transform(X_scaled)
        clusters = self.kmeans.fit_predict(X_pca)

        return X_scaled, X_pca, clusters

    # -----------------------------
    # Visualization
    # -----------------------------
    def plot_3d(self, X_pca: np.ndarray, clusters: np.ndarray, save_name="phase_space.png"):
        """
        3D regime geometry visualization
        """

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")

        scatter = ax.scatter(
            X_pca[:, 0],
            X_pca[:, 1],
            X_pca[:, 2],
            c=clusters,
            cmap="viridis",
            s=30,
            alpha=0.8
        )

        ax.set_title("ICCS v0.4 — Regime Phase Space (PCA 3D)")
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_zlabel("PC3")

        legend = ax.legend(*scatter.legend_elements(), title="Regimes")
        ax.add_artist(legend)

        output_path = os.path.join(self.output_dir, save_name)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    # -----------------------------
    # Save results
    # -----------------------------
    def save_results(self, df, X_pca, clusters):
        out = df.copy()
        out["PC1"] = X_pca[:, 0]
        out["PC2"] = X_pca[:, 1]
        out["PC3"] = X_pca[:, 2]
        out["regime_cluster"] = clusters

        path = os.path.join(self.output_dir, "regime_labeled.csv")
        out.to_csv(path, index=False)

        return path

    # -----------------------------
    # Full run
    # -----------------------------
    def run(self, benchmark_path: str):
        """
        Main entry point
        """

        df = self.load_benchmark(benchmark_path)
        X = self.build_feature_matrix(df)

        X_scaled, X_pca, clusters = self.fit(X)

        plot_path = self.plot_3d(X_pca, clusters)
        csv_path = self.save_results(df, X_pca, clusters)

        return {
            "plot": plot_path,
            "csv": csv_path,
            "n_samples": len(df),
            "n_features": X.shape[1],
            "n_clusters": self.n_clusters
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="benchmark output file (.csv or .json)")
    parser.add_argument("--clusters", type=int, default=3)

    args = parser.parse_args()

    engine = RegimeGeometry(n_clusters=args.clusters)
    result = engine.run(args.input)

    print(json.dumps(result, indent=2))
