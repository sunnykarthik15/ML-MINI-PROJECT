"""
Exploratory Data Analysis (EDA) and Model Evaluation Module.

Provides:
1. EDA visualizations:
   - Class distribution bar chart
   - Article length distribution histogram
   - Top words in REAL news
   - Top words in FAKE news
2. Comprehensive Model Evaluation:
   - Accuracy, Precision, Recall, F1-Score (macro & weighted)
   - Confusion matrix visualizations saved to results/confusion_matrices/
   - Full classification reports saved to results/metrics/
   - Model comparison CSV saved to results/metrics/model_comparison.csv
3. Dynamic Model Selection:
   - Identifies highest F1-score model
   - Saves final model as models/final_model.pkl
   - Generates models/model_metadata.json with all evaluation statistics
"""

import os
import json
from collections import Counter
from typing import Dict, Any, List, Tuple
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Style settings for clean, academic aesthetic plots
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
PALETTE = {"REAL": "#2b8a3e", "FAKE": "#c92a2a"}


def generate_eda_reports_and_plots(
    df: pd.DataFrame,
    output_dir: str = "results/eda"
) -> Dict[str, Any]:
    """
    Performs Exploratory Data Analysis and generates required visualizations.

    Generates:
    1. Class distribution bar chart (class_distribution.png)
    2. Article length distribution (article_length_distribution.png)
    3. Top words in REAL news (top_words_real.png)
    4. Top words in FAKE news (top_words_fake.png)
    """
    print("\n--- Generating Exploratory Data Analysis (EDA) ---")
    os.makedirs(output_dir, exist_ok=True)

    total_records = len(df)
    class_counts = df["label"].value_counts().to_dict()
    df["char_count"] = df["full_text"].str.len()
    df["word_count"] = df["full_text"].apply(lambda x: len(x.split()))

    stats = {
        "total_records": total_records,
        "class_distribution": class_counts,
        "avg_char_length": float(df["char_count"].mean()),
        "avg_word_count": float(df["word_count"].mean()),
        "real_avg_words": float(df[df["label"] == "REAL"]["word_count"].mean()),
        "fake_avg_words": float(df[df["label"] == "FAKE"]["word_count"].mean()),
    }

    print(f"[EDA] Total Cleaned Records: {total_records}")
    print(f"[EDA] Class Breakdown: {class_counts}")
    print(f"[EDA] Average Word Count - REAL: {stats['real_avg_words']:.1f} words, FAKE: {stats['fake_avg_words']:.1f} words")

    # 1. Class Distribution Bar Chart
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(
        x=list(class_counts.keys()),
        y=list(class_counts.values()),
        hue=list(class_counts.keys()),
        palette=[PALETTE.get(k, "#4dabf7") for k in class_counts.keys()],
        legend=False
    )
    plt.title("Distribution of REAL vs. FAKE News Articles", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("News Category", fontsize=11)
    plt.ylabel("Number of Articles", fontsize=11)
    for p in ax.patches:
        count = int(p.get_height())
        pct = (count / total_records) * 100
        ax.annotate(f"{count:,}\n({pct:.1f}%)", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha="center", va="center", fontsize=11, color="white", fontweight="bold")
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "class_distribution.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"[EDA] Saved: '{chart_path}'")

    # 2. Article Length (Word Count) Distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=df[df["word_count"] <= 2500],
        x="word_count",
        hue="label",
        bins=50,
        kde=True,
        palette=PALETTE,
        alpha=0.6
    )
    plt.title("Article Word Count Distribution by Class (Up to 2,500 words)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Word Count", fontsize=11)
    plt.ylabel("Article Frequency", fontsize=11)
    plt.tight_layout()
    len_path = os.path.join(output_dir, "article_length_distribution.png")
    plt.savefig(len_path, dpi=300)
    plt.close()
    print(f"[EDA] Saved: '{len_path}'")

    # Helper function to get top words
    def _plot_top_words(label_val: str, filename: str, title: str, bar_color: str):
        subset = df[df["label"] == label_val]["full_text"]
        words = []
        for text in subset:
            words.extend(text.split())
        counts = Counter(words).most_common(20)
        word_df = pd.DataFrame(counts, columns=["word", "frequency"])

        plt.figure(figsize=(8, 6))
        sns.barplot(data=word_df, y="word", x="frequency", color=bar_color)
        plt.title(title, fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Frequency Count", fontsize=11)
        plt.ylabel("Token / Word", fontsize=11)
        plt.tight_layout()
        save_file = os.path.join(output_dir, filename)
        plt.savefig(save_file, dpi=300)
        plt.close()
        print(f"[EDA] Saved: '{save_file}'")

    # 3 & 4. Top Words Plots
    _plot_top_words("REAL", "top_words_real.png", "Top 20 Frequent Words in REAL News", PALETTE["REAL"])
    _plot_top_words("FAKE", "top_words_fake.png", "Top 20 Frequent Words in FAKE News", PALETTE["FAKE"])

    print("--- Exploratory Data Analysis Completed ---\n")
    return stats


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
    output_dir: str = "results/confusion_matrices"
) -> str:
    """Plot and save a clean, annotated confusion matrix."""
    os.makedirs(output_dir, exist_ok=True)
    labels = ["REAL", "FAKE"]
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar=False,
        annot_kws={"size": 13, "weight": "bold"}
    )
    plt.title(f"Confusion Matrix: {model_name}", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()

    safe_name = model_name.lower().replace(" ", "_")
    output_path = os.path.join(output_dir, f"{safe_name}_cm.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def evaluate_all_models(
    models: Dict[str, Any],
    X_test_tfidf,
    y_test: pd.Series,
    metrics_dir: str = "results/metrics",
    cm_dir: str = "results/confusion_matrices"
) -> pd.DataFrame:
    """
    Evaluates each model strictly on the held-out test set.
    Calculates Accuracy, Precision, Recall, F1-Score.
    Generates confusion matrices and classification reports.
    """
    print("\n--- Starting Model Evaluation on Test Set ---")
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs(cm_dir, exist_ok=True)

    results_list = []

    for name, model in models.items():
        print(f"\n[Evaluation] Evaluating: {name}...")
        y_pred = model.predict(X_test_tfidf)

        acc = float(accuracy_score(y_test, y_pred))
        # Use macro average across REAL and FAKE classes
        prec = float(precision_score(y_test, y_pred, average="macro"))
        rec = float(recall_score(y_test, y_pred, average="macro"))
        f1 = float(f1_score(y_test, y_pred, average="macro"))

        print(f"  - Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
        print(f"  - Precision: {prec:.4f}")
        print(f"  - Recall:    {rec:.4f}")
        print(f"  - F1 Score:  {f1:.4f}")

        # Save classification report
        report_text = classification_report(y_test, y_pred, target_names=["FAKE", "REAL"], digits=4)
        safe_name = name.lower().replace(" ", "_")
        report_path = os.path.join(metrics_dir, f"{safe_name}_classification_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Classification Report: {name}\n")
            f.write("=" * 60 + "\n\n")
            f.write(report_text)

        # Plot confusion matrix
        cm_path = plot_confusion_matrix(y_test, y_pred, name, output_dir=cm_dir)
        print(f"  - Confusion Matrix saved to '{cm_path}'")

        results_list.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1 Score": round(f1, 4),
            "model_object": model,
            "report_path": report_path,
            "cm_path": cm_path
        })

    # Create comparison DataFrame
    comparison_df = pd.DataFrame(results_list)
    export_df = comparison_df[["Model", "Accuracy", "Precision", "Recall", "F1 Score"]]

    comparison_csv_path = os.path.join(metrics_dir, "model_comparison.csv")
    export_df.to_csv(comparison_csv_path, index=False)
    print(f"\n[Evaluation] Model comparison saved to '{comparison_csv_path}':")
    print(export_df.to_string(index=False))

    return comparison_df


def select_and_save_final_model(
    comparison_df: pd.DataFrame,
    dataset_info: Dict[str, Any],
    models_dir: str = "models"
) -> Dict[str, Any]:
    """
    Selects the best model primarily based on highest test F1-Score
    (with Precision and Recall as tiebreakers), saves it to models/final_model.pkl,
    and writes models/model_metadata.json.
    """
    print("\n--- Dynamic Model Selection ---")
    # Sort primarily by F1 Score descending, then Precision, then Recall
    sorted_df = comparison_df.sort_values(
        by=["F1 Score", "Precision", "Recall"],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    winner_row = sorted_df.iloc[0]
    winner_name = winner_row["Model"]
    winner_f1 = winner_row["F1 Score"]
    winner_acc = winner_row["Accuracy"]
    winner_prec = winner_row["Precision"]
    winner_rec = winner_row["Recall"]
    winner_obj = winner_row["model_object"]

    print(f"[Selection] Best-performing model: '{winner_name}'")
    print(f"[Selection] Performance -> F1-Score: {winner_f1:.4f}, Accuracy: {winner_acc:.4f}, Precision: {winner_prec:.4f}, Recall: {winner_rec:.4f}")

    # Save final model
    os.makedirs(models_dir, exist_ok=True)
    final_model_path = os.path.join(models_dir, "final_model.pkl")
    joblib.dump(winner_obj, final_model_path)
    print(f"[Selection] Saved best model to: '{final_model_path}'")

    # Generate metadata
    metadata = {
        "selected_model": winner_name,
        "selection_criteria": "Highest Macro F1-Score on isolated test set (80/20 stratified split)",
        "metrics": {
            "accuracy": float(winner_acc),
            "precision": float(winner_prec),
            "recall": float(winner_rec),
            "f1_score": float(winner_f1)
        },
        "all_models_compared": [
            {
                "model": row["Model"],
                "accuracy": float(row["Accuracy"]),
                "precision": float(row["Precision"]),
                "recall": float(row["Recall"]),
                "f1_score": float(row["F1 Score"])
            }
            for _, row in sorted_df.iterrows()
        ],
        "training_configuration": {
            "test_split_ratio": 0.20,
            "stratified": True,
            "random_state": 42,
            "vectorizer": {
                "algorithm": "TF-IDF (TfidfVectorizer)",
                "max_features": 5000,
                "ngram_range": [1, 2],
                "sublinear_tf": True
            }
        },
        "dataset_summary": dataset_info
    }

    metadata_path = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"[Selection] Metadata saved to: '{metadata_path}'")
    print("--- Dynamic Model Selection Completed ---\n")

    return metadata
