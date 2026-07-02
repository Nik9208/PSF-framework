import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run(cmd, title):
    print("\n" + "=" * 80)
    print(f"[ICCS PIPELINE] {title}")
    print("=" * 80)

    start = time.time()
    result = subprocess.run(cmd, shell=True, cwd=BASE_DIR)

    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {title}")

    print(f"[OK] {title} completed in {time.time() - start:.2f}s\n")


def main():
    print("\n🚀 ICCS v1.0 FULL PIPELINE STARTED\n")

    # 1. Debug falsification suite
    run(
        "python experiments/iccs_debug_harness.py",
        "DEBUG HARNESS (Null Collapse Test)"
    )

    # 2. Extended benchmarks
    run(
        "python experiments/iccs_extended_benchmark.py",
        "EXTENDED BENCHMARKS"
    )

    # 3. Full evaluation against baselines
    run(
        "python experiments/iccs_evaluation_harness.py",
        "EVALUATION HARNESS (Baselines comparison)"
    )

    # 4. Visualization layer
    run(
        "python experiments/iccs_results_visualizer.py",
        "RESULT VISUALIZATION PIPELINE"
    )

    print("\n🎯 ICCS v1.0 PIPELINE COMPLETE")
    print("Results written to /results and /iccs_figures")


if __name__ == "__main__":
    main()
