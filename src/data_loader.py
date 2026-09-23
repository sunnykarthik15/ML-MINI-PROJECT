"""
Data Loading and Cleaning Module for Fake News Detection.

Handles:
- Loading raw CSV datasets (supports Option A: title/text/label, and Option B: True.csv/Fake.csv)
- Column detection and validation
- Missing value handling
- Duplicate removal
- Combining title and text into a unified full_text column
- Normalizing labels to exactly 'REAL' and 'FAKE'
- Saving the cleaned dataset to data/processed/cleaned_news.csv
"""

import os
import sys
from typing import Optional, Tuple
import pandas as pd


def detect_and_load_raw_data(raw_dir: str = "data/raw") -> pd.DataFrame:
    """
    Detect dataset in raw_dir and load into a unified DataFrame.

    Supports:
    1. Single CSV with title, text, label (Option A)
    2. Two CSVs: True.csv and Fake.csv (Option B)
    3. Any CSV file in raw_dir containing text and label columns.
    """
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Raw data directory '{raw_dir}' does not exist.")

    files = [f for f in os.listdir(raw_dir) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError(
            f"No CSV dataset found in '{raw_dir}'. "
            f"Please place a fake news CSV dataset in '{raw_dir}'."
        )

    # Option B check: ISOT style True.csv and Fake.csv
    true_file = next((f for f in files if f.lower() in ["true.csv", "real.csv"]), None)
    fake_file = next((f for f in files if f.lower() in ["fake.csv"]), None)
    if true_file and fake_file:
        print(f"[DataLoader] Detected Option B dataset: '{true_file}' and '{fake_file}'.")
        df_true = pd.read_csv(os.path.join(raw_dir, true_file))
        df_fake = pd.read_csv(os.path.join(raw_dir, fake_file))
        df_true["label"] = "REAL"
        df_fake["label"] = "FAKE"
        combined_df = pd.concat([df_true, df_fake], ignore_index=True)
        return combined_df

    # Option A / Single CSV check
    target_csv = None
    preferred_names = ["fake_or_real_news.csv", "news.csv", "fake_news.csv", "train.csv", "dataset.csv"]
    for pref in preferred_names:
        if pref in files:
            target_csv = pref
            break
    if not target_csv:
        target_csv = files[0]

    filepath = os.path.join(raw_dir, target_csv)
    print(f"[DataLoader] Loading raw dataset from '{filepath}'...")
    df = pd.read_csv(filepath)
    return df


def normalize_labels(series: pd.Series) -> pd.Series:
    """
    Map various label formats (0/1, 'true'/'fake', 'real'/'fake') to 'REAL' / 'FAKE'.
    """
    def _map_val(val):
        if pd.isna(val):
            return None
        val_str = str(val).strip().upper()
        if val_str in ["REAL", "TRUE", "1", "1.0", "GENUINE"]:
            return "REAL"
        elif val_str in ["FAKE", "FALSE", "0", "0.0", "FABRICATED"]:
            return "FAKE"
        return None

    return series.apply(_map_val)


def clean_and_prepare_dataset(
    df: pd.DataFrame,
    output_path: str = "data/processed/cleaned_news.csv"
) -> pd.DataFrame:
    """
    Cleans raw DataFrame, normalizes columns and labels, and saves cleaned CSV.

    Args:
        df: Raw DataFrame
        output_path: Path to write cleaned CSV

    Returns:
        pd.DataFrame: Cleaned DataFrame with columns ['full_text', 'label']
    """
    print("\n--- Starting Data Loading and Cleaning ---")
    initial_rows = len(df)
    print(f"[DataLoader] Initial raw dataset rows: {initial_rows}")

    # Standardize column names (lowercase)
    col_mapping = {c: c.lower().strip() for c in df.columns}
    df = df.rename(columns=col_mapping)

    # Detect label column
    label_col = None
    candidate_label_cols = ["label", "target", "class", "category", "output"]
    for col in candidate_label_cols:
        if col in df.columns:
            label_col = col
            break

    if not label_col:
        raise ValueError(
            f"Could not identify a label column in dataset. Available columns: {list(df.columns)}"
        )

    # Detect text and title columns
    text_col = next((c for c in ["text", "article", "content", "body", "news"] if c in df.columns), None)
    title_col = next((c for c in ["title", "headline", "header"] if c in df.columns), None)

    if not text_col and not title_col:
        raise ValueError(
            f"Dataset must contain at least 'text' or 'title' column. Columns: {list(df.columns)}"
        )

    print(f"[DataLoader] Detected columns -> Label: '{label_col}', Text: '{text_col}', Title: '{title_col}'")

    # Combine title and text if both present
    if title_col and text_col:
        title_series = df[title_col].fillna("").astype(str)
        text_series = df[text_col].fillna("").astype(str)
        combined_text = (title_series + " " + text_series).str.strip()
    elif text_col:
        combined_text = df[text_col].fillna("").astype(str).str.strip()
    else:
        combined_text = df[title_col].fillna("").astype(str).str.strip()

    cleaned_df = pd.DataFrame({
        "full_text": combined_text,
        "label": normalize_labels(df[label_col])
    })

    # Drop missing labels or empty text
    before_na_drop = len(cleaned_df)
    cleaned_df = cleaned_df.dropna(subset=["label"])
    cleaned_df = cleaned_df[cleaned_df["full_text"].str.len() > 10]
    dropped_na = before_na_drop - len(cleaned_df)
    if dropped_na > 0:
        print(f"[DataLoader] Removed {dropped_na} records with missing/empty text or invalid labels.")

    # Remove duplicates
    before_dup_drop = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["full_text"])
    dropped_dup = before_dup_drop - len(cleaned_df)
    if dropped_dup > 0:
        print(f"[DataLoader] Removed {dropped_dup} duplicate news articles.")

    # Ensure strictly two classes: REAL and FAKE
    unique_classes = set(cleaned_df["label"].unique())
    if unique_classes != {"REAL", "FAKE"}:
        raise ValueError(
            f"Expected binary classification with classes {{'REAL', 'FAKE'}}, but found {unique_classes}"
        )

    # Dataset dimensions & distribution
    final_rows = len(cleaned_df)
    class_counts = cleaned_df["label"].value_counts().to_dict()
    print(f"[DataLoader] Final cleaned dataset dimensions: {cleaned_df.shape}")
    print("[DataLoader] Class distribution:")
    for cls_name, count in class_counts.items():
        pct = (count / final_rows) * 100
        print(f"  - {cls_name}: {count} ({pct:.2f}%)")

    # Save to data/processed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)
    print(f"[DataLoader] Cleaned dataset saved successfully to: '{output_path}'")
    print("--- Data Loading and Cleaning Completed ---\n")

    return cleaned_df


def load_dataset(raw_dir: str = "data/raw", processed_path: str = "data/processed/cleaned_news.csv") -> pd.DataFrame:
    """
    High-level entry point to load or generate the cleaned dataset.
    """
    raw_df = detect_and_load_raw_data(raw_dir)
    cleaned_df = clean_and_prepare_dataset(raw_df, output_path=processed_path)
    return cleaned_df


if __name__ == "__main__":
    load_dataset()
