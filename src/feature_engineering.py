"""
Feature Engineering Module for Fake News Detection.

Implements:
- Stratified 80/20 train/test split with a fixed random_state
- TF-IDF Vectorization using sklearn.feature_extraction.text.TfidfVectorizer
- STRICT DATA-LEAKAGE PREVENTION:
    - Vectorizer is fitted ONLY on the training split (X_train)
    - Test split (X_test) is transformed using the already-fitted vectorizer
- Saving and loading the fitted TF-IDF vectorizer using joblib
"""

import os
from typing import Tuple, Optional
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


def split_dataset(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Split the dataset into training and testing sets with stratification.

    Args:
        df: DataFrame containing 'full_text' and 'label' columns.
        test_size: Proportion of dataset for test set (default: 0.2 -> 80% train, 20% test).
        random_state: Seed for reproducibility.

    Returns:
        Tuple: X_train, X_test, y_train, y_test
    """
    print(f"\n[FeatureEngineering] Splitting data: {100 - int(test_size*100)}% train / {int(test_size*100)}% test (stratified, random_state={random_state})...")
    X = df["full_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    print(f"[FeatureEngineering] Training samples: {len(X_train)} ({y_train.value_counts().to_dict()})")
    print(f"[FeatureEngineering] Testing samples:  {len(X_test)} ({y_test.value_counts().to_dict()})")
    return X_train, X_test, y_train, y_test


def create_vectorizer(
    max_features: int = 5000,
    ngram_range: Tuple[int, int] = (1, 2),
    min_df: int = 3,
    max_df: float = 0.9,
    sublinear_tf: bool = True
) -> TfidfVectorizer:
    """
    Instantiate a TfidfVectorizer configured appropriately for news articles.

    Parameters explained:
    - max_features (5000): Restricts vocabulary to top 5,000 most informative terms, avoiding curse of dimensionality.
    - ngram_range (1, 2): Extracts unigrams and bigrams, capturing phrase context (e.g. 'breaking news', 'white house').
    - min_df (3): Ignores rare terms appearing in fewer than 3 documents (filters typos/noise).
    - max_df (0.9): Ignores corpus-specific ubiquitous words appearing in >90% of documents.
    - sublinear_tf (True): Uses 1 + log(tf) scaling to dampen the effect of very frequent words.
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf
    )
    return vectorizer


def fit_and_transform_features(
    X_train: pd.Series,
    X_test: pd.Series,
    vectorizer: Optional[TfidfVectorizer] = None,
    save_path: str = "models/tfidf_vectorizer.pkl"
) -> Tuple[object, object, TfidfVectorizer]:
    """
    Fits TF-IDF strictly on X_train, transforms both X_train and X_test, and saves the vectorizer.

    Data-Leakage Rule:
    - Vectorizer is fitted strictly on X_train.
    - X_test is transformed using the fitted vectorizer; no test information leaks into the vocabulary or IDF weights.
    """
    if vectorizer is None:
        vectorizer = create_vectorizer()

    print("[FeatureEngineering] Fitting TF-IDF Vectorizer ONLY on training set (X_train)...")
    X_train_tfidf = vectorizer.fit_transform(X_train)
    print(f"[FeatureEngineering] X_train_tfidf shape: {X_train_tfidf.shape}")

    print("[FeatureEngineering] Transforming testing set (X_test) with fitted vectorizer...")
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"[FeatureEngineering] X_test_tfidf shape:  {X_test_tfidf.shape}")

    # Save fitted vectorizer
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(vectorizer, save_path)
        print(f"[FeatureEngineering] Fitted TF-IDF vectorizer saved to: '{save_path}'")

    return X_train_tfidf, X_test_tfidf, vectorizer


def load_vectorizer(model_path: str = "models/tfidf_vectorizer.pkl") -> TfidfVectorizer:
    """Load pre-fitted TF-IDF vectorizer from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Vectorizer file not found at '{model_path}'. Please train the model first.")
    return joblib.load(model_path)
