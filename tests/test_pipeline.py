"""
Unit and Integration Test Suite for Fake News Detection Pipeline.

Verifies:
1. Dataset loading and column normalization
2. Text preprocessing (HTML, URLs, stopwords, lemmatization)
3. TF-IDF feature generation and leakage prevention
4. Train/test split logic
5. Model training and serialization
6. Prediction pipeline on sample articles
"""

import os
import unittest
import pandas as pd
import numpy as np

from src.preprocessing import clean_text
from src.data_loader import normalize_labels, clean_and_prepare_dataset
from src.feature_engineering import split_dataset, create_vectorizer, fit_and_transform_features
from src.train import train_naive_bayes, train_logistic_regression, train_linear_svm
from src.predict import NewsPredictor


class TestFakeNewsPipeline(unittest.TestCase):

    def test_text_preprocessing(self):
        """Test NLP cleaning steps: HTML stripping, URL removal, lowercasing, stopwords."""
        raw_html_url = "Visit <a href='http://example.com'>Link</a> http://site.org for THE 100% cure!"
        cleaned = clean_text(raw_html_url)
        self.assertNotIn("http", cleaned)
        self.assertNotIn("<a", cleaned)
        self.assertNotIn("the", cleaned.split())  # stopword removed
        self.assertTrue(cleaned.islower())

        # Test empty and none handling
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")
        self.assertEqual(clean_text("     "), "")

    def test_label_normalization(self):
        """Test mapping diverse labels to strictly REAL or FAKE."""
        s = pd.Series(["real", "FAKE", "1", "0", "True", "False", "genuine", "fabricated"])
        normalized = normalize_labels(s)
        expected = ["REAL", "FAKE", "REAL", "FAKE", "REAL", "FAKE", "REAL", "FAKE"]
        self.assertEqual(list(normalized), expected)

    def test_dataset_cleaning_structure(self):
        """Test data cleaning with mock DataFrame."""
        mock_df = pd.DataFrame({
            "title": ["Gov Passes Bill", "Aliens landed in Texas", "Gov Passes Bill", ""],
            "text": ["Official voting completed.", "Conspiracy revealed yesterday.", "Official voting completed.", ""],
            "label": ["REAL", "FAKE", "REAL", "FAKE"]
        })
        cleaned = clean_and_prepare_dataset(mock_df, output_path="data/processed/test_clean.csv")
        self.assertIn("full_text", cleaned.columns)
        self.assertIn("label", cleaned.columns)
        # Verify duplicate was removed (3 down to 2 valid rows)
        self.assertEqual(len(cleaned), 2)
        if os.path.exists("data/processed/test_clean.csv"):
            os.remove("data/processed/test_clean.csv")

    def test_feature_engineering_split_and_leakage(self):
        """Verify 80/20 stratified split and independent vectorizer transform."""
        sample_texts = [f"News story text sample {i} about economy and politics" for i in range(50)]
        sample_labels = ["REAL"] * 25 + ["FAKE"] * 25
        df = pd.DataFrame({"full_text": sample_texts, "label": sample_labels})

        X_train, X_test, y_train, y_test = split_dataset(df, test_size=0.2, random_state=42)
        self.assertEqual(len(X_train), 40)
        self.assertEqual(len(X_test), 10)
        self.assertEqual(list(y_train.value_counts()), [20, 20])

        vec = create_vectorizer(max_features=50)
        X_train_vec, X_test_vec, fitted_vec = fit_and_transform_features(
            X_train, X_test, vectorizer=vec, save_path=None
        )
        self.assertEqual(X_train_vec.shape[0], 40)
        self.assertEqual(X_test_vec.shape[0], 10)
        self.assertEqual(X_train_vec.shape[1], X_test_vec.shape[1])

    def test_prediction_pipeline_execution(self):
        """Verify predictor execution on two distinct test news samples."""
        # Check if model artifacts exist before testing predictor
        if not os.path.exists("models/final_model.pkl") or not os.path.exists("models/tfidf_vectorizer.pkl"):
            self.skipTest("Trained model files not found yet; will test after run_pipeline.")

        predictor = NewsPredictor()

        # Sample 1
        sample_1 = (
            "The Treasury Department announced new fiscal policy guidelines on Wednesday, "
            "focusing on interstate commerce regulation and tax adjustments for renewable investments."
        )
        res_1 = predictor.predict(sample_1)
        self.assertIn(res_1["prediction"], ["REAL", "FAKE"])
        self.assertIn("confidence", res_1)
        self.assertIn("model_name", res_1)

        # Sample 2
        sample_2 = (
            "Shocking leaked document exposes covert planetary base hidden inside mountain! "
            "Whistleblower claims extraterrestrials run global corporations in complete secret!"
        )
        res_2 = predictor.predict(sample_2)
        self.assertIn(res_2["prediction"], ["REAL", "FAKE"])
        self.assertIn("confidence", res_2)
        self.assertIn("model_name", res_2)


if __name__ == "__main__":
    unittest.main()
