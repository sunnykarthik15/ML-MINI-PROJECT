"""
Prediction Pipeline for Fake News Detection.

Loads the saved best model (models/final_model.pkl) and fitted TF-IDF vectorizer
(models/tfidf_vectorizer.pkl), preprocesses incoming raw news text, and generates
a classification of 'REAL' or 'FAKE' along with technical model confidence.

Note on Terminology:
- Uses 'Model Confidence' strictly to denote statistical probability or margin.
- Never refers to 'truth probability' as this system classifies linguistic patterns
  and does not independently verify factual claims.
"""

import os
import sys
import argparse
import json
from typing import Dict, Any, Optional
import joblib
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from src.preprocessing import clean_text
except ImportError:
    from preprocessing import clean_text


class NewsPredictor:
    """Predictor class encapsulating vectorizer, model, and inference logic."""

    def __init__(
        self,
        model_path: str = "models/final_model.pkl",
        vectorizer_path: str = "models/tfidf_vectorizer.pkl",
        metadata_path: str = "models/model_metadata.json"
    ):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.metadata_path = metadata_path
        self.model = None
        self.vectorizer = None
        self.model_name = "Classical ML Model"
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Load serialized model and vectorizer from disk."""
        model_path = self.model_path
        if not os.path.exists(model_path):
            alt_path = os.path.join(PROJECT_ROOT, self.model_path)
            if os.path.exists(alt_path):
                model_path = alt_path
            else:
                raise FileNotFoundError(
                    f"Model file not found at '{self.model_path}'. "
                    f"Please run the pipeline first: python run_pipeline.py"
                )

        vec_path = self.vectorizer_path
        if not os.path.exists(vec_path):
            alt_vec = os.path.join(PROJECT_ROOT, self.vectorizer_path)
            if os.path.exists(alt_vec):
                vec_path = alt_vec
            else:
                raise FileNotFoundError(
                    f"TF-IDF vectorizer not found at '{self.vectorizer_path}'. "
                    f"Please run the pipeline first: python run_pipeline.py"
                )

        meta_path = self.metadata_path
        if not os.path.exists(meta_path):
            alt_meta = os.path.join(PROJECT_ROOT, self.metadata_path)
            if os.path.exists(alt_meta):
                meta_path = alt_meta

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vec_path)

        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    self.model_name = meta.get("selected_model", type(self.model).__name__)
            except Exception:
                self.model_name = type(self.model).__name__
        else:
            self.model_name = type(self.model).__name__

    def predict(self, raw_text: str) -> Dict[str, Any]:
        """
        Classify raw news text as REAL or FAKE.

        Args:
            raw_text (str): News article title or body.

        Returns:
            Dict containing:
                - prediction: 'REAL' or 'FAKE'
                - confidence: Technical confidence percentage or decision margin
                - probability: Float probability if supported, else None
                - model_name: Name of selected model
                - cleaned_text_preview: Snippet of cleaned text used for inference
                - disclaimer: Educational disclaimer
        """
        if not raw_text or not isinstance(raw_text, str) or len(raw_text.strip()) == 0:
            return {
                "prediction": "INVALID",
                "confidence": "N/A",
                "probability": None,
                "model_name": self.model_name,
                "cleaned_text_preview": "",
                "error": "Input text is empty or invalid.",
                "disclaimer": "Please provide a valid news article text."
            }

        # 1. Apply identical preprocessing
        cleaned = clean_text(raw_text)
        if not cleaned:
            return {
                "prediction": "INVALID",
                "confidence": "N/A",
                "probability": None,
                "model_name": self.model_name,
                "cleaned_text_preview": "",
                "error": "Text became empty after removing stopwords, numbers, and symbols.",
                "disclaimer": "Please provide meaningful textual news content."
            }

        # 2. Extract TF-IDF features using pre-fitted vectorizer
        features = self.vectorizer.transform([cleaned])

        # 3. Generate prediction
        prediction = self.model.predict(features)[0]

        # 4. Compute model confidence
        confidence_str = "N/A"
        probability_val = None

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(features)[0]
            classes = list(self.model.classes_)
            pred_idx = classes.index(prediction)
            prob = float(probs[pred_idx])
            probability_val = prob
            confidence_str = f"{prob * 100:.2f}%"
        elif hasattr(self.model, "decision_function"):
            # Linear SVM decision score (distance to separating hyperplane)
            dist = float(self.model.decision_function(features)[0])
            # Apply standard sigmoid to get calibrated probability estimate: 1 / (1 + exp(-dist))
            prob = 1.0 / (1.0 + np.exp(-abs(dist)))
            probability_val = prob
            confidence_str = f"{prob * 100:.2f}% (Margin: {dist:+.2f})"

        disclaimer = (
            "NOTICE: This classification is generated by a classical machine learning model "
            "trained on linguistic patterns. It is an academic demonstration and does NOT "
            "independently verify the factual truth or source authenticity of the article."
        )

        preview = cleaned[:120] + ("..." if len(cleaned) > 120 else "")

        return {
            "prediction": prediction,
            "confidence": confidence_str,
            "probability": probability_val,
            "model_name": self.model_name,
            "cleaned_text_preview": preview,
            "disclaimer": disclaimer
        }


def predict_news(text: str) -> Dict[str, Any]:
    """Helper function to instantiate predictor and run prediction."""
    predictor = NewsPredictor()
    return predictor.predict(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict whether a news article is REAL or FAKE.")
    parser.add_argument("--text", type=str, help="Raw news article text or headline")
    args = parser.parse_args()

    sample_text = args.text
    if not sample_text:
        sample_text = (
            "Congress passed the annual federal spending bill on Thursday afternoon, "
            "averting a partial government shutdown after bipartisan negotiations."
        )
        print("[Predict] No --text argument supplied. Using default sample text.")

    print(f"\n[Predict] Input Text:\n\"{sample_text}\"\n")
    try:
        predictor = NewsPredictor()
        result = predictor.predict(sample_text)
        print("=" * 50)
        print(f"PREDICTION:       {result['prediction']}")
        print(f"MODEL CONFIDENCE: {result['confidence']}")
        print(f"SELECTED MODEL:   {result['model_name']}")
        print("=" * 50)
        print(f"NOTE: {result['disclaimer']}\n")
    except Exception as e:
        print(f"Error during prediction: {e}")
        sys.exit(1)
