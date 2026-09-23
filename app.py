"""
Streamlit Web Application for Fake News Detection.

BTech CSE Academic Mini-Project.
NLP-based classification using TF-IDF and classical machine learning.
Loads pre-trained model and vectorizer without retraining.
"""

import os
import json
import streamlit as st
import pandas as pd
from PIL import Image

from src.predict import NewsPredictor

# Page Configuration
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Academic & Professional Polish
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .result-box-real {
        background-color: #ecfdf5;
        border-left: 6px solid #10b981;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .result-box-fake {
        background-color: #fef2f2;
        border-left: 6px solid #ef4444;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .metric-badge {
        display: inline-block;
        font-size: 0.9rem;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        background-color: #f1f5f9;
        color: #334155;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .disclaimer-card {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        padding: 0.9rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #92400e;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading trained machine learning model...")
def get_predictor():
    """Load and cache the trained prediction pipeline."""
    return NewsPredictor()


@st.cache_data
def get_metadata():
    """Load model metadata and metrics summary."""
    meta_path = "models/model_metadata.json"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


@st.cache_data
def get_comparison_data():
    """Load model comparison metrics CSV."""
    comp_path = "results/metrics/model_comparison.csv"
    if os.path.exists(comp_path):
        return pd.read_csv(comp_path)
    return None


def main():
    # Sidebar
    with st.sidebar:
        st.header("📌 Project Details")
        st.markdown("**BTech CSE Machine Learning Mini-Project**")
        st.markdown("**Domain:** Natural Language Processing (NLP)")

        meta = get_metadata()
        if meta:
            st.divider()
            st.subheader("Selected Model")
            st.write(f"🏆 **{meta.get('selected_model', 'N/A')}**")
            metrics = meta.get("metrics", {})
            st.write(f"• **Accuracy:** `{metrics.get('accuracy', 0)*100:.2f}%`")
            st.write(f"• **F1-Score:** `{metrics.get('f1_score', 0):.4f}`")
            st.write(f"• **Precision:** `{metrics.get('precision', 0):.4f}`")
            st.write(f"• **Recall:** `{metrics.get('recall', 0):.4f}`")

            st.divider()
            ds_info = meta.get("dataset_summary", {})
            st.subheader("Dataset Info")
            st.write(f"• **Source:** `{ds_info.get('dataset_name', 'fake_or_real_news.csv')}`")
            st.write(f"• **Total Cleaned:** `{ds_info.get('total_records_cleaned', 0):,}`")
            st.write(f"• **REAL Articles:** `{ds_info.get('real_count', 0):,}`")
            st.write(f"• **FAKE Articles:** `{ds_info.get('fake_count', 0):,}`")
            st.write("• **Split:** 80% Train / 20% Test (Stratified)")

        st.divider()
        st.caption("Anti-Leakage Guaranteed: TF-IDF fitted strictly on training data.")

    # Main Header
    st.markdown('<div class="main-header">Fake News Detection Using Natural Language Processing and Machine Learning</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">NLP-based classification using TF-IDF and classical machine learning algorithms</div>', unsafe_allow_html=True)

    # Check if model exists
    if not os.path.exists("models/final_model.pkl") or not os.path.exists("models/tfidf_vectorizer.pkl"):
        st.error("⚠️ Model artifacts not found. Please execute the training pipeline first using: `python run_pipeline.py`")
        st.stop()

    predictor = get_predictor()

    # Pre-defined test sample buttons for quick viva demonstration
    st.markdown("##### 🧪 Quick Test Samples (Click to load):")
    col_sample1, col_sample2, col_clear = st.columns([1, 1, 1])

    sample_real = (
        "WASHINGTON — The Senate voted overwhelmingly on Thursday to confirm the new director of "
        "the Federal Bureau of Investigation, following weeks of bipartisan committee hearings. "
        "Lawmakers from both parties praised the nominee's career credentials in public service and law."
    )
    sample_fake = (
        "BREAKING SECRET LEAK: Proof emerges that government elites are secretly spraying microscopic "
        "chips through aircraft contrails to manipulate public voting preferences in the upcoming election! "
        "Whistleblower reveals suppressed documents mainstream media refuses to show!"
    )

    if "article_input" not in st.session_state:
        st.session_state["article_input"] = ""

    if col_sample1.button("📄 Load Real News Example"):
        st.session_state["article_input"] = sample_real

    if col_sample2.button("⚠️ Load Fake News Example"):
        st.session_state["article_input"] = sample_fake

    if col_clear.button("🗑️ Clear Input"):
        st.session_state["article_input"] = ""

    # News Input Form
    user_input = st.text_area(
        label="Paste News Article Headline and Body Text:",
        value=st.session_state["article_input"],
        height=180,
        placeholder="Enter or paste the complete news article text here for analysis..."
    )

    col_btn, _ = st.columns([1, 3])
    predict_clicked = col_btn.button("🔍 Classify Article", type="primary", use_container_width=True)

    if predict_clicked:
        if not user_input.strip():
            st.warning("Please enter or paste news article text before clicking Classify.")
        else:
            with st.spinner("Analyzing text patterns using classical NLP & ML..."):
                res = predictor.predict(user_input)

            if res.get("prediction") == "INVALID":
                st.error(res.get("error", "Invalid input."))
            else:
                pred = res["prediction"]
                conf = res["confidence"]
                model_used = res["model_name"]
                cleaned_preview = res["cleaned_text_preview"]

                if pred == "REAL":
                    st.markdown(f"""
                    <div class="result-box-real">
                        <h2 style="color: #065f46; margin: 0 0 0.5rem 0;">Prediction: REAL NEWS (GENUINE)</h2>
                        <span class="metric-badge">Model Confidence: {conf}</span>
                        <span class="metric-badge">Classifier: {model_used}</span>
                        <p style="margin-top: 0.8rem; color: #064e3b; font-size: 0.95rem;">
                            The article matches linguistic and lexical characteristics typical of authentic journalistic reporting in the training corpus.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-box-fake">
                        <h2 style="color: #991b1b; margin: 0 0 0.5rem 0;">Prediction: FAKE NEWS (FABRICATED)</h2>
                        <span class="metric-badge">Model Confidence: {conf}</span>
                        <span class="metric-badge">Classifier: {model_used}</span>
                        <p style="margin-top: 0.8rem; color: #7f1d1d; font-size: 0.95rem;">
                            The article exhibits linguistic characteristics, sensationalist cues, or patterns commonly associated with fabricated news in the training corpus.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with st.expander("🔍 View Preprocessed NLP Tokens Used for Classification"):
                    st.code(cleaned_preview, language="text")

                # Academic Warning / Limitation Card
                st.markdown(f"""
                <div class="disclaimer-card">
                    <strong>⚠️ Academic Limitation & Technical Note:</strong><br>
                    {res['disclaimer']}
                </div>
                """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # Academic Project Documentation Tabs
    tab_explain, tab_eval, tab_eda = st.tabs(["📚 Model Explanations (Viva Notes)", "📊 Model Comparison & Confusion Matrix", "📈 Exploratory Data Analysis (EDA)"])

    with tab_explain:
        st.subheader("Core Academic Concepts Explained")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 1. TF-IDF (Term Frequency-Inverse Document Frequency)
            - **What it does:** Converts unstructured text into numerical feature vectors.
            - **Formula:** $\\text{TF-IDF}(t, d, D) = \\text{TF}(t, d) \\times \\text{IDF}(t, D)$
            - **TF:** Measures how frequently term $t$ appears in document $d$.
            - **IDF:** $\\log(\\frac{1 + |D|}{1 + |\\{d \\in D : t \\in d\\}|}) + 1$. Downweights ubiquitous words (e.g. *said*, *year*) while giving higher weights to distinctive, topic-specific terms.
            - **Why it fits news:** Effectively captures informative unigram and bigram vocabulary while remaining computationally lightweight and explainable.

            ### 2. Multinomial Naive Bayes
            - **Concept:** Probabilistic classifier grounded in Bayes' Theorem:
              $$P(c|d) \\propto P(c) \\prod_{i=1}^n P(w_i|c)$$
            - **Independence Assumption:** Assumes word occurrences are conditionally independent given the class label.
            - **Strength:** Extremely fast training, effective with sparse word count vectors, highly resistant to overfitting on high dimensions.
            """)

        with col2:
            st.markdown("""
            ### 3. Logistic Regression
            - **Concept:** Parametric linear classifier predicting class probability using a sigmoid function:
              $$P(y=\\text{REAL}|x) = \\frac{1}{1 + e^{-(w^T x + b)}}$$
            - **Decision Boundary:** Learns optimal linear weights $w$ via maximum likelihood estimation (Log-Loss).
            - **Strength:** Highly explainable, directly provides calibrated posterior probabilities, and excels on linear text classification tasks.

            ### 4. Linear Support Vector Machine (Linear SVM)
            - **Concept:** Non-probabilistic binary classifier that determines the maximum-margin hyperplane separating REAL from FAKE feature representations:
              $$\\min_{w, b} \\frac{1}{2} \\|w\\|^2 + C \\sum_{i} \\max(0, 1 - y_i(w^T x_i + b))$$
            - **Strength:** Exceptional generalization in high-dimensional sparse TF-IDF spaces; robust to high feature-to-sample ratios.
            """)

    with tab_eval:
        st.subheader("Comparative Model Performance on Test Set (20% Stratified)")
        comp_df = get_comparison_data()
        if comp_df is not None:
            st.dataframe(
                comp_df.style.highlight_max(subset=["Accuracy", "Precision", "Recall", "F1 Score"], color="#bbf7d0"),
                use_container_width=True
            )
        else:
            st.info("Comparison data will appear after running the pipeline.")

        st.markdown("#### Test Confusion Matrices")
        cm_cols = st.columns(3)
        cm_files = [
            ("Multinomial Naive Bayes", "results/confusion_matrices/multinomial_naive_bayes_cm.png"),
            ("Logistic Regression", "results/confusion_matrices/logistic_regression_cm.png"),
            ("Linear SVM", "results/confusion_matrices/linear_svm_cm.png")
        ]

        for idx, (m_name, cm_path) in enumerate(cm_files):
            with cm_cols[idx]:
                st.caption(f"**{m_name}**")
                if os.path.exists(cm_path):
                    st.image(Image.open(cm_path), use_container_width=True)
                else:
                    st.info("Confusion matrix plot pending.")

    with tab_eda:
        st.subheader("Exploratory Data Analysis Figures")
        eda_cols1, eda_cols2 = st.columns(2)

        with eda_cols1:
            st.caption("Class Distribution")
            p1 = "results/eda/class_distribution.png"
            if os.path.exists(p1):
                st.image(Image.open(p1), use_container_width=True)

            st.caption("Top Frequent Words in REAL News")
            p3 = "results/eda/top_words_real.png"
            if os.path.exists(p3):
                st.image(Image.open(p3), use_container_width=True)

        with eda_cols2:
            st.caption("Article Word Count Distribution")
            p2 = "results/eda/article_length_distribution.png"
            if os.path.exists(p2):
                st.image(Image.open(p2), use_container_width=True)

            st.caption("Top Frequent Words in FAKE News")
            p4 = "results/eda/top_words_fake.png"
            if os.path.exists(p4):
                st.image(Image.open(p4), use_container_width=True)


if __name__ == "__main__":
    main()
