import numpy as np
import pandas as pd

from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# =========================================================
# REAL ICCS WRAPPER FROM DEBUG HARNESS
# =========================================================
class RawICCSPipeline:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        
    def fit_predict(self, X):
        if X.shape[1] < 3:
            # Embed using delay embedding if 1D
            if X.shape[1] == 1:
                delay = 1
                # pad or slice carefully
                X_emb = np.column_stack([X[:-2*delay], X[delay:-delay], X[2*delay:]])
                # to keep labels same size as input for ARI:
                # pad with first/last values
                pad_front = np.zeros((delay, 3))
                pad_back = np.zeros((delay, 3))
                # we'll just slice the whole dataset for evaluation to match shapes later
            else:
                X_emb = X
        else:
            X_emb = X
            
        X_scaled = StandardScaler().fit_transform(X_emb)
        pca = PCA(n_components=min(3, X_scaled.shape[1]))
        X_pca = pca.fit_transform(X_scaled)
        
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        labels = kmeans.fit_predict(X_pca)
        return labels

# =========================================================
# 1. HMM (simple Gaussian emission proxy)
# =========================================================
class SimpleHMM:

    def fit_predict(self, X, n_states=3):
        X = StandardScaler().fit_transform(X)

        # proxy: GMM ≈ HMM baseline approximation
        model = GaussianMixture(n_components=n_states, random_state=42)
        return model.fit_predict(X)


# =========================================================
# 2. Koopman-style proxy (spectral dynamics embedding)
# =========================================================
class KoopmanProxy:

    def fit_predict(self, X, n_clusters=3):
        X = StandardScaler().fit_transform(X)

        # time-delay embedding (very simplified Koopman surrogate)
        X_embed = np.column_stack([
            X[:-2],
            X[1:-1],
            X[2:]
        ])

        model = GaussianMixture(n_components=n_clusters, random_state=42)
        return model.fit_predict(X_embed)


# =========================================================
# 3. Change point detection (simplified BOCPD-style proxy)
# =========================================================
class ChangePointBaseline:

    def fit_predict(self, X, window=20):
        X = X.flatten()

        scores = []

        for i in range(len(X)):
            start = max(0, i - window)
            segment = X[start:i+1]

            score = np.std(segment)
            scores.append(score)

        scores = np.array(scores)

        # discretize into regimes
        threshold = np.percentile(scores, 50)
        return (scores > threshold).astype(int)


# =========================================================
# 4. ICCS vs ALL BASELINES COMPARISON
# =========================================================
class ICCSBenchmarkSuite:

    def __init__(self, iccs_model):
        self.iccs = iccs_model

        self.hmm = SimpleHMM()
        self.koopman = KoopmanProxy()
        self.cp = ChangePointBaseline()

    def evaluate(self, X, name="dataset"):
        # Match lengths for delay embeddings
        # Koopman and ICCS with delay will be len(X)-2
        
        iccs_labels = self.iccs.fit_predict(X)
        
        # if ICCS used delay embedding, it drops 2 samples. 
        # If X was > 1D (like Lorenz), it doesn't.
        drop_iccs = len(X) - len(iccs_labels)

        hmm_labels = self.hmm.fit_predict(X)
        koop_labels = self.koopman.fit_predict(X) # koop_labels is len(X)-2
        cp_labels = self.cp.fit_predict(X)

        # Truncate all to the shortest length
        min_len = min(len(iccs_labels), len(hmm_labels), len(koop_labels), len(cp_labels))
        
        iccs_labels = iccs_labels[:min_len]
        hmm_labels = hmm_labels[:min_len]
        koop_labels = koop_labels[:min_len]
        cp_labels = cp_labels[:min_len]

        results = {
            "dataset": name,

            # agreement with baselines
            "ARI_iccs_hmm": adjusted_rand_score(iccs_labels, hmm_labels),
            "ARI_iccs_koopman": adjusted_rand_score(iccs_labels, koop_labels),
            "ARI_iccs_changepoint": adjusted_rand_score(iccs_labels, cp_labels),

            # baseline agreement (sanity)
            "ARI_hmm_koopman": adjusted_rand_score(hmm_labels, koop_labels)
        }

        return results

    def run(self, datasets):
        out = []

        for name, X in datasets.items():
            out.append(self.evaluate(X, name))

        return pd.DataFrame(out)


# =========================================================
# 5. ENTRY POINT
# =========================================================
if __name__ == "__main__":
    from iccs_evaluation_harness import DatasetLoader

    datasets = {
        "logistic": DatasetLoader.logistic_map(),
        "lorenz": DatasetLoader.lorenz(),
        "brownian": DatasetLoader.brownian()
    }

    suite = ICCSBenchmarkSuite(RawICCSPipeline())
    results = suite.run(datasets)

    print("\n=== EXTENDED BASELINE COMPARISON ===")
    print(results.to_string())
    results.to_csv("results/outputs/extended_benchmark_results.csv", index=False)
