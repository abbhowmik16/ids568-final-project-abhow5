"""
Drift Detection for RAG Observable Signals
Component 4: Data Integrity & Drift Detection

Detects drift in:
1. Query length
2. Retrieval distance
3. Response length
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_psi(reference, current, n_bins=10):
    ref = np.array(reference)
    cur = np.array(current)

    _, bin_edges = np.histogram(ref, bins=n_bins)

    ref_counts, _ = np.histogram(ref, bins=bin_edges)
    cur_counts, _ = np.histogram(cur, bins=bin_edges)

    ref_pct = (ref_counts + 1) / (len(ref) + n_bins)
    cur_pct = (cur_counts + 1) / (len(cur) + n_bins)

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return float(psi)


def severity_from_psi(psi):
    if psi < 0.1:
        return "none"
    elif psi < 0.2:
        return "moderate"
    return "significant"


def simulate_rag_observations(seed=42):
    np.random.seed(seed)

    n = 500

    reference = pd.DataFrame({
        "query_length_tokens": np.random.normal(8, 2, n).clip(1),
        "retrieval_distance": np.random.normal(0.75, 0.12, n).clip(0),
        "response_length_chars": np.random.normal(180, 45, n).clip(20),
    })

    current = pd.DataFrame({
        "query_length_tokens": np.random.normal(13, 3, n).clip(1),
        "retrieval_distance": np.random.normal(1.05, 0.18, n).clip(0),
        "response_length_chars": np.random.normal(260, 70, n).clip(20),
    })

    return reference, current


def plot_feature(reference, current, feature, psi):
    Path("visualizations").mkdir(exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.hist(reference[feature], bins=25, alpha=0.6, label="Reference")
    plt.hist(current[feature], bins=25, alpha=0.6, label="Current")
    plt.title(f"Drift Comparison: {feature} | PSI={psi:.3f}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

    output_path = Path(f"visualizations/drift_{feature}.png")
    plt.savefig(output_path, dpi=150)
    plt.close()

    return str(output_path)


def main():
    print("=" * 60)
    print("RAG DRIFT DETECTION")
    print("=" * 60)

    reference, current = simulate_rag_observations()

    results = []

    for feature in reference.columns:
        psi = calculate_psi(reference[feature], current[feature])
        severity = severity_from_psi(psi)
        plot_path = plot_feature(reference, current, feature, psi)

        result = {
            "feature": feature,
            "reference_mean": round(float(reference[feature].mean()), 3),
            "current_mean": round(float(current[feature].mean()), 3),
            "psi": round(psi, 3),
            "severity": severity,
            "visualization": plot_path,
        }

        results.append(result)

        print(json.dumps(result, indent=2))

    summary = {
        "features_analyzed": len(results),
        "significant_drift_features": [
            r["feature"] for r in results if r["severity"] == "significant"
        ],
        "moderate_drift_features": [
            r["feature"] for r in results if r["severity"] == "moderate"
        ],
        "recommendation": "Investigate retrieval quality and refresh knowledge base if retrieval distance remains elevated.",
    }

    output = {
        "summary": summary,
        "results": results,
    }

    Path("logs").mkdir(exist_ok=True)
    Path("logs/drift_detection_results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )

    print("\nSUMMARY")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()