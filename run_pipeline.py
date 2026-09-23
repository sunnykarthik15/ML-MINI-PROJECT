"""
Master End-to-End Execution Pipeline for Fake News Detection.

Executes the academic ML workflow in strict logical order:
1. Validates and loads raw dataset from data/raw/
2. Cleans dataset and handles missing values/duplicates -> data/processed/cleaned_news.csv
3. Applies reusable NLP preprocessing (lowercasing, cleaning, tokenization, lemmatization)
4. Executes Exploratory Data Analysis (EDA) and outputs 4 visualization figures -> results/eda/
5. Performs stratified 80/20 train/test split
6. Fits TF-IDF strictly on training data (preventing data leakage) -> models/tfidf_vectorizer.pkl
7. Trains 3 classical ML models: Naive Bayes, Logistic Regression, Linear SVM -> models/*.pkl
8. Evaluates all models on held-out test set -> results/metrics/ and results/confusion_matrices/
9. Exports model comparison table -> results/metrics/model_comparison.csv
10. Dynamically selects best model by Macro F1-Score -> models/final_model.pkl & models/model_metadata.json
11. Verifies prediction pipeline on sample test articles
"""

import os
import sys
import time
import pandas as pd

from src.data_loader import load_dataset
from src.preprocessing import clean_text, setup_nltk_resources
from src.feature_engineering import split_dataset, fit_and_transform_features
from src.train import train_all_models
from src.evaluate import generate_eda_reports_and_plots, evaluate_all_models, select_and_save_final_model
from src.predict import NewsPredictor


def run_pipeline() -> None:
    start_time = time.time()
    print("=" * 70)
    print("  FAKE NEWS DETECTION MACHINE LEARNING PIPELINE")
    print("  BTech CSE Academic Mini-Project")
    print("=" * 70)

    # 1. Dataset Verification
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir) or not [f for f in os.listdir(raw_dir) if f.endswith(".csv")]:
        print(f"\n[ERROR] Missing required dataset in '{raw_dir}'.")
        print("Please place an authentic fake-news CSV dataset (e.g. fake_or_real_news.csv) inside 'data/raw/'.")
        sys.exit(1)

    # 2. Data Loading & Cleaning
    processed_csv = "data/processed/cleaned_news.csv"
    df = load_dataset(raw_dir=raw_dir, processed_path=processed_csv)

    # 3. NLP Preprocessing
    print("\n--- Starting NLP Preprocessing ---")
    setup_nltk_resources()
    total_docs = len(df)
    print(f"[Preprocessing] Processing {total_docs:,} articles (lowercasing, punctuation/URL removal, tokenization, lemmatization)...")

    preprocessed_texts = []
    log_interval = max(1000, total_docs // 5)
    for idx, text in enumerate(df["full_text"]):
        preprocessed_texts.append(clean_text(text))
        if (idx + 1) % log_interval == 0 or (idx + 1) == total_docs:
            print(f"  Processed {idx + 1:,} / {total_docs:,} articles...")

    df["full_text"] = preprocessed_texts

    # Drop any records that became empty after text normalization
    valid_mask = df["full_text"].str.strip().str.len() > 5
    if (~valid_mask).sum() > 0:
        print(f"[Preprocessing] Dropping {(~valid_mask).sum()} articles that became empty post-cleaning.")
        df = df[valid_mask].reset_index(drop=True)

    print(f"[Preprocessing] Final preprocessed dataset size: {len(df):,} articles.")
    print("--- NLP Preprocessing Completed ---")

    # 4. Exploratory Data Analysis (EDA)
    eda_stats = generate_eda_reports_and_plots(df.copy(), output_dir="results/eda")

    # 5. Train / Test Split (80% Train, 20% Test, Stratified, random_state=42)
    X_train, X_test, y_train, y_test = split_dataset(df, test_size=0.20, random_state=42)

    # 6. TF-IDF Feature Engineering (Strictly fit on X_train only)
    X_train_tfidf, X_test_tfidf, vectorizer = fit_and_transform_features(
        X_train=X_train,
        X_test=X_test,
        save_path="models/tfidf_vectorizer.pkl"
    )

    # 7. Model Training (Naive Bayes, Logistic Regression, Linear SVM)
    trained_models = train_all_models(X_train_tfidf, y_train, models_dir="models")

    # 8 & 9. Model Evaluation and Comparison
    comparison_df = evaluate_all_models(
        models=trained_models,
        X_test_tfidf=X_test_tfidf,
        y_test=y_test,
        metrics_dir="results/metrics",
        cm_dir="results/confusion_matrices"
    )

    # 10. Dynamic Model Selection & Final Model Saving
    dataset_summary = {
        "dataset_name": "fake_or_real_news.csv",
        "total_records_cleaned": len(df),
        "real_count": int((df["label"] == "REAL").sum()),
        "fake_count": int((df["label"] == "FAKE").sum()),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "eda_stats": eda_stats
    }

    metadata = select_and_save_final_model(
        comparison_df=comparison_df,
        dataset_info=dataset_summary,
        models_dir="models"
    )

    # 11. Verification Test
    print("\n--- Verifying Inference Pipeline ---")
    predictor = NewsPredictor()

    sample_articles = [
        (
            "NASA Mars Rover Discovers Evidence of Ancient Microbial Habitat",
            "Scientists analyzing data from NASA's Curiosity rover have identified organic compounds "
            "and geological formations consistent with ancient habitable lake beds on Mars, according "
            "to peer-reviewed findings published in the journal Nature Geoscience."
        ),
        (
            "Secret Celebrity Underground Bunker Revealed with Alien Technology",
            "Shocking leaked government memos disclose an underground base where Hollywood elites "
            "and reptilian hybrids communicate with outer space entities using forbidden microchips. "
            "Mainstream media is refusing to air this shocking truth!"
        )
    ]

    for title, body in sample_articles:
        full_sample = f"{title}. {body}"
        res = predictor.predict(full_sample)
        print(f"\n[Test Article] \"{title}\"")
        print(f"  -> Prediction:       {res['prediction']}")
        print(f"  -> Model Confidence: {res['confidence']}")
        print(f"  -> Selected Model:   {res['model_name']}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"  ALL PIPELINE STAGES COMPLETED SUCCESSFULLY IN {elapsed:.2f}s")
    print(f"  Selected Best Model: {metadata['selected_model']}")
    print(f"  Best Test Macro F1:  {metadata['metrics']['f1_score']:.4f}")
    print(f"  Best Test Accuracy:  {metadata['metrics']['accuracy'] * 100:.2f}%")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_pipeline()
