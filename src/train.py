"""
Model Training Module for Fake News Detection.

Trains three classical Machine Learning algorithms on TF-IDF features:
1. Multinomial Naive Bayes (MultinomialNB)
2. Logistic Regression (LogisticRegression)
3. Linear Support Vector Machine (LinearSVC)

Saves each trained model in the models/ directory using joblib.
"""

import os
from typing import Dict, Any
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


def train_naive_bayes(
    X_train,
    y_train,
    alpha: float = 0.1
) -> MultinomialNB:
    """
    Train a Multinomial Naive Bayes model.

    MultinomialNB uses Bayes' Theorem with strong independence assumptions:
    P(c|d) ∝ P(c) * ∏ P(w_i|c).
    Alpha provides Laplace smoothing to prevent zero probabilities for unseen n-grams.
    """
    print(f"\n[Training] Training Multinomial Naive Bayes (alpha={alpha})...")
    model = MultinomialNB(alpha=alpha)
    model.fit(X_train, y_train)
    print("[Training] Multinomial Naive Bayes training complete.")
    return model


def train_logistic_regression(
    X_train,
    y_train,
    C: float = 1.0,
    max_iter: int = 1000,
    random_state: int = 42
) -> LogisticRegression:
    """
    Train a Logistic Regression model.

    Logistic Regression learns a linear decision boundary mapped through a sigmoid
    function to predict log-odds of a class:
    P(y=REAL|x) = 1 / (1 + exp(-(w^T x + b))).
    """
    print(f"\n[Training] Training Logistic Regression (C={C}, max_iter={max_iter})...")
    model = LogisticRegression(C=C, max_iter=max_iter, random_state=random_state)
    model.fit(X_train, y_train)
    print("[Training] Logistic Regression training complete.")
    return model


def train_linear_svm(
    X_train,
    y_train,
    C: float = 1.0,
    random_state: int = 42
) -> LinearSVC:
    """
    Train a Linear Support Vector Machine (LinearSVC).

    Linear SVM finds the optimal maximum-margin separating hyperplane
    between REAL and FAKE article representations in high-dimensional TF-IDF space.
    """
    print(f"\n[Training] Training Linear Support Vector Machine (LinearSVC, C={C})...")
    model = LinearSVC(C=C, random_state=random_state, dual="auto")
    model.fit(X_train, y_train)
    print("[Training] Linear Support Vector Machine training complete.")
    return model


def train_all_models(
    X_train,
    y_train,
    models_dir: str = "models"
) -> Dict[str, Any]:
    """
    Train all three classical ML models and save them to models_dir.

    Returns:
        Dict[str, Any]: Map of model name to fitted model object.
    """
    os.makedirs(models_dir, exist_ok=True)

    models = {
        "Multinomial Naive Bayes": train_naive_bayes(X_train, y_train),
        "Logistic Regression": train_logistic_regression(X_train, y_train),
        "Linear SVM": train_linear_svm(X_train, y_train),
    }

    # Save trained models
    model_filenames = {
        "Multinomial Naive Bayes": "naive_bayes.pkl",
        "Logistic Regression": "logistic_regression.pkl",
        "Linear SVM": "linear_svm.pkl",
    }

    for name, model in models.items():
        filename = model_filenames[name]
        save_path = os.path.join(models_dir, filename)
        joblib.dump(model, save_path)
        print(f"[Training] Saved {name} model to '{save_path}'")

    return models
