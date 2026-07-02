import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score

from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")


# =========================================================
# 1. BASELINE MODELS
# =========================================================

class Baselines:

    @staticmethod
    def pca_gmm(X, n_clusters=3):
        X = StandardScaler().fit_transform(X)
        Xp = PCA(n_components=min(3, X.shape[1])).fit_transform(X)

        gmm = GaussianMixture(n_components=n_clusters, random_state=42)
        labels = gmm.fit_predict(Xp)

        return labels


    @staticmethod
    def spectral_clustering(X, n_clusters=3):
        X = StandardScaler().fit_transform(X)

        model = SpectralClustering(
            n_clusters=n_clusters,
            affinity="nearest_neighbors",
            assign_labels="kmeans",
            random_state=42
        )

        return model.fit_predict(X)


# =========================================================
# 2. ICCS WRAPPER (plug-in interface)
# =========================================================

class ICCSAdapter:

    def __init__(self, iccs_pipeline):
        self.pipeline = iccs_pipeline

    def run(self, X):
        """
        Expected ICCS pipeline output:
        must return labels OR regime assignment
        """
        return self.pipeline.fit_predict(X)


# =========================================================
# 3. DATASETS
# =========================================================

class DatasetLoader:

    # -------------------------
    # Tier 1: Synthetic chaos
    # -------------------------

    @staticmethod
    def logistic_map(n=1000, r=3.9, x0=0.5):
        x = np.zeros(n)
        x[0] = x0

        for t in range(1, n):
            x[t] = r * x[t-1] * (1 - x[t-1])

        return x.reshape(-1, 1)


    @staticmethod
    def lorenz(n=2000, dt=0.01):
        sigma, beta, rho = 10, 2.667, 28

        x, y, z = 1.0, 1.0, 1.0
        out = []

        for _ in range(n):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z

            x += dx * dt
            y += dy * dt
            z += dz * dt

            out.append([x, y, z])

        return np.array(out)


    @staticmethod
    def brownian(n=1000):
        return np.cumsum(np.random.randn(n)).reshape(-1, 1)


    @staticmethod
    def shuffled_surrogate(X):
        X = X.copy()
        np.random.shuffle(X)
        return X


# =========================================================
# 4. FALSIFICATION METRICS
# =========================================================

class FalsificationMetrics:

    @staticmethod
    def structural_falsification_score(labels):
        """
        Penalize over-segmentation on random-like data
        """
        unique = len(np.unique(labels))
        return unique


    @staticmethod
    def stability_score(labels):
        """
        Measure regime persistence
        """
        changes = np.sum(np.diff(labels) != 0)
        return 1.0 / (1.0 + changes)


    @staticmethod
    def compare_to_baseline(iccs_labels, baseline_labels):
        return adjusted_rand_score(iccs_labels, baseline_labels)


# =========================================================
# 5. EVALUATION HARNESS CORE
# =========================================================

class ICCSEvaluationHarness:

    def __init__(self, iccs_model):
        self.iccs = ICCSAdapter(iccs_model)

    # -------------------------
    # generic evaluation
    # -------------------------
    def evaluate(self, X, name="dataset"):
        print(f"\n=== Evaluating: {name} ===")

        # ICCS
        iccs_labels = self.iccs.run(X)

        # Baselines
        pca_gmm_labels = Baselines.pca_gmm(X)
        spectral_labels = Baselines.spectral_clustering(X)

        # Metrics
        results = {
            "dataset": name,

            # structural falsification
            "iccs_complexity": FalsificationMetrics.structural_falsification_score(iccs_labels),
            "baseline_complexity": FalsificationMetrics.structural_falsification_score(pca_gmm_labels),

            # stability
            "iccs_stability": FalsificationMetrics.stability_score(iccs_labels),
            "baseline_stability": FalsificationMetrics.stability_score(pca_gmm_labels),

            # agreement with baselines
            "ari_iccs_pca_gmm": FalsificationMetrics.compare_to_baseline(iccs_labels, pca_gmm_labels),
            "ari_iccs_spectral": FalsificationMetrics.compare_to_baseline(iccs_labels, spectral_labels),
        }

        return results

    # -------------------------
    # full benchmark suite
    # -------------------------
    def run_full_suite(self):

        results = []

        # Tier 1
        X1 = DatasetLoader.logistic_map()
        X2 = DatasetLoader.lorenz()
        X3 = DatasetLoader.brownian()

        results.append(self.evaluate(X1, "logistic_map"))
        results.append(self.evaluate(X2, "lorenz_system"))
        results.append(self.evaluate(X3, "brownian_motion"))

        # surrogate test
        results.append(self.evaluate(DatasetLoader.shuffled_surrogate(X1), "shuffled_logistic"))

        return pd.DataFrame(results)


# =========================================================
# 6. ENTRY POINT
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # Placeholder ICCS model adapter
    # Replace with real pipeline:
    # regime_geometry + transition + curvature + control
    # -----------------------------------------------------

    class DummyICCS:

        def fit_predict(self, X):
            # simple proxy: thresholding for structure simulation
            return (X[:, 0] > np.median(X[:, 0])).astype(int)

    harness = ICCSEvaluationHarness(DummyICCS())

    results = harness.run_full_suite()

    print("\n=== FINAL RESULTS ===")
    print(results.to_string())
    
    results.to_csv("results/outputs/evaluation_results.csv", index=False)
    print("\nSaved to evaluation_results.csv")
