import os
import pandas as pd
import matplotlib.pyplot as plt


class ICCSResultsVisualizer:

    def __init__(self, output_dir="iccs_figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # Load evaluation results
    # -----------------------------
    def load_results(self, path):
        return pd.read_csv(path)

    # -----------------------------
    # 1. Complexity comparison
    # -----------------------------
    def plot_complexity(self, df):
        plt.figure()

        plt.bar(df["dataset"], df["iccs_complexity"], label="ICCS")
        plt.bar(df["dataset"], df["baseline_complexity"], alpha=0.5, label="Baseline")

        plt.title("Structural Complexity Comparison")
        plt.ylabel("Complexity Score")
        plt.xticks(rotation=30)
        plt.legend()

        path = os.path.join(self.output_dir, "complexity.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()

        return path

    # -----------------------------
    # 2. Stability comparison
    # -----------------------------
    def plot_stability(self, df):
        plt.figure()

        plt.plot(df["dataset"], df["iccs_stability"], marker="o", label="ICCS")
        plt.plot(df["dataset"], df["baseline_stability"], marker="x", label="Baseline")

        plt.title("Regime Stability Comparison")
        plt.ylabel("Stability Score")
        plt.xticks(rotation=30)
        plt.legend()

        path = os.path.join(self.output_dir, "stability.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()

        return path

    # -----------------------------
    # 3. Agreement (ARI)
    # -----------------------------
    def plot_agreement(self, df):
        plt.figure()

        plt.plot(df["dataset"], df["ari_iccs_pca_gmm"], marker="o", label="ICCS vs PCA+GMM")
        plt.plot(df["dataset"], df["ari_iccs_spectral"], marker="x", label="ICCS vs Spectral")

        plt.title("Regime Agreement (ARI)")
        plt.ylabel("Adjusted Rand Index")
        plt.xticks(rotation=30)
        plt.legend()

        path = os.path.join(self.output_dir, "agreement.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()

        return path

    # -----------------------------
    # 4. Combined dashboard summary
    # -----------------------------
    def plot_dashboard(self, df):
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # Complexity
        axes[0].bar(df["dataset"], df["iccs_complexity"])
        axes[0].set_title("Complexity")

        # Stability
        axes[1].plot(df["dataset"], df["iccs_stability"], marker="o")
        axes[1].set_title("Stability")

        # Agreement
        axes[2].plot(df["dataset"], df["ari_iccs_pca_gmm"])
        axes[2].set_title("ARI")

        for ax in axes:
            ax.tick_params(axis='x', rotation=30)

        plt.tight_layout()

        path = os.path.join(self.output_dir, "dashboard.png")
        plt.savefig(path, dpi=300)
        plt.close()

        return path

    # -----------------------------
    # Full pipeline
    # -----------------------------
    def run(self, results_csv_path):
        df = self.load_results(results_csv_path)

        outputs = {
            "complexity_plot": self.plot_complexity(df),
            "stability_plot": self.plot_stability(df),
            "agreement_plot": self.plot_agreement(df),
            "dashboard": self.plot_dashboard(df)
        }

        return outputs


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    visualizer = ICCSResultsVisualizer()

    # expects output of evaluation harness saved as CSV
    results = visualizer.run("evaluation_results.csv")

    print("\n=== VISUALIZATION OUTPUTS ===")
    for k, v in results.items():
        print(k, "->", v)
