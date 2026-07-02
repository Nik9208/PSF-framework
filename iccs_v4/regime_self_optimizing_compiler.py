import os
import json
import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances


class SelfOptimizingRegimeCompiler:
    """
    Module H — ICCS v1.0 Meta-Learning Layer

    Objective:
    - optimize internal representation of ICCS pipeline
    - minimize collapse energy (from Module F)
    - maximize regime separability and stability
    """

    def __init__(
        self,
        n_clusters_range=(3, 8),
        pca_components_range=(2, 4),
        alpha=0.5,
        output_dir="meta_compiler_output"
    ):
        self.n_clusters_range = n_clusters_range
        self.pca_components_range = pca_components_range
        self.alpha = alpha

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load raw benchmark data
    # -----------------------------
    def load_data(self, path):
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            import json
            with open(path, "r", encoding="utf-8") as f:
                df = pd.DataFrame(json.load(f))
        else:
            raise ValueError("Unsupported format")

        return df.select_dtypes(include=[np.number]).dropna()

    # -----------------------------
    # Collapse proxy (unsupervised)
    # -----------------------------
    def collapse_energy(self, X):
        """
        Proxy for instability:
        - mean pairwise distance variance
        """

        D = pairwise_distances(X)
        return float(np.var(D))

    # -----------------------------
    # Evaluate configuration
    # -----------------------------
    def evaluate(self, X, n_components, n_clusters):
        """
        One ICCS configuration trial
        """

        pca = PCA(n_components=n_components)
        Xp = pca.fit_transform(X)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(Xp)

        energy = self.collapse_energy(Xp)

        # separability proxy: cluster centroid spread
        centroids = np.array([Xp[labels == i].mean(axis=0) for i in range(n_clusters)])
        separation = float(np.mean(pairwise_distances(centroids)))

        # stability score (higher is better)
        score = separation - self.alpha * energy

        return {
            "n_components": n_components,
            "n_clusters": n_clusters,
            "energy": energy,
            "separation": separation,
            "score": score
        }

    # -----------------------------
    # Search best geometry
    # -----------------------------
    def optimize(self, X):
        results = []

        # Bound n_components_range based on number of features
        n_features = X.shape[1]
        max_comp = min(self.pca_components_range[1], n_features)
        min_comp = min(self.pca_components_range[0], max_comp)

        # Bound n_clusters_range based on number of samples
        n_samples = X.shape[0]
        max_clus = min(self.n_clusters_range[1], n_samples - 1)
        min_clus = min(self.n_clusters_range[0], max_clus)

        for c in range(min_comp, max_comp + 1):
            for k in range(min_clus, max_clus + 1):
                res = self.evaluate(X, c, k)
                results.append(res)

        if not results:
             # fallback if too few samples/features
             return {"n_components": min_comp, "n_clusters": min_clus, "energy": 0, "separation": 0, "score": 0}, []

        best = max(results, key=lambda x: x["score"])

        return best, results

    # -----------------------------
    # Apply best configuration
    # -----------------------------
    def apply(self, X, config):
        pca = PCA(n_components=config["n_components"])
        Xp = pca.fit_transform(X)

        kmeans = KMeans(n_clusters=config["n_clusters"], random_state=42)
        labels = kmeans.fit_predict(Xp)

        return Xp, labels

    # -----------------------------
    # Full pipeline
    # -----------------------------
    def run(self, benchmark_path):
        X = self.load_data(benchmark_path)

        best, history = self.optimize(X)
        Xp, labels = self.apply(X, best)

        result = {
            "best_config": best,
            "history": history
        }

        out_path = os.path.join(self.output_dir, "meta_compiler_summary.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return {
            "summary": out_path,
            "best_config": best
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    engine = SelfOptimizingRegimeCompiler()
    result = engine.run(args.input)

    print(json.dumps(result, indent=2))
