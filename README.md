# Fake News Detection Using NLP and Machine Learning

**An Academic Machine Learning Mini-Project (BTech CSE)**  
NLP-based classification using TF-IDF and classical machine learning algorithms.

---

## 1. Project Overview
With the exponential growth of online journalism and social media dissemination, distinguishing authentic news from fabricated stories has become a significant technical challenge. This project implements an academic Natural Language Processing (NLP) and Machine Learning (ML) system that analyzes the linguistic patterns, terminology, and syntax of news articles to classify them as either **REAL** or **FAKE**.

Designed specifically as a clean, explainable, and reproducible BTech CSE mini-project, the system avoids complex black-box deep learning or external APIs in favor of classical, interpretable NLP techniques and statistical classifiers.

---

## 2. Problem Statement
The proliferation of misinformation ("fake news") poses serious societal, political, and economic risks. Readers often cannot manually verify every claim. The computational challenge is:  
*Given the title and textual content of an unverified news article, can a machine learning model accurately classify it as genuine reporting or fabricated content based solely on learned textual patterns?*

---

## 3. Objective
1. Build an end-to-end classical NLP and ML classification pipeline without data leakage.
2. Clean, normalize, and preprocess raw unstructured news text using standard NLP methods.
3. Conduct Exploratory Data Analysis (EDA) to understand vocabulary differences and length distributions.
4. Extract numerical features using Term Frequency-Inverse Document Frequency (TF-IDF).
5. Train and comparatively evaluate three classical machine learning algorithms:
   - **Multinomial Naive Bayes**
   - **Logistic Regression**
   - **Linear Support Vector Machine (Linear SVM)**
6. Dynamically select the best-performing model based on test Macro F1-score.
7. Provide an interactive, academic Streamlit web interface for demonstration and viva examinations.

---

## 4. Technologies Used
- **Language:** Python 3.11
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning & Metrics:** Scikit-learn
- **Natural Language Processing:** NLTK (Stopwords, WordNet Lemmatizer, Punkt)
- **Data Visualization:** Matplotlib, Seaborn
- **Model Serialization:** Joblib
- **Web Interface:** Streamlit

---

## 5. Dataset
The project utilizes the authentic, widely-cited benchmark news dataset (`fake_or_real_news.csv` collected by George McIntire and Katharine Jarmul).
- **Source:** Benchmark news corpus
- **Total Raw Articles:** 6,335
- **Duplicates Removed:** 29
- **Cleaned Dataset Records:** 6,306
- **Class Balance:**
  - **REAL Articles:** 3,154 (50.02%)
  - **FAKE Articles:** 3,152 (49.98%)

---

## 6. Dataset Format
The data loader natively supports two standard dataset formats:

### Option A (Single CSV - Used by default):
CSV file located in `data/raw/` with the following columns:
- `title`: Headline or title of the news story (string)
- `text`: Body content of the news article (string)
- `label`: Target class (`REAL` or `FAKE`, also supports `0`/`1`, `True`/`False`)

### Option B (ISOT Dual-CSV Format):
Directory `data/raw/` containing:
- `True.csv`: Contains authentic news articles (`title`, `text`, `subject`, `date`)
- `Fake.csv`: Contains fabricated news articles (`title`, `text`, `subject`, `date`)

---

## 7. Project Architecture

```
Raw News Dataset (CSV)
         │
         ▼
[ Data Loading & Cleaning ]  ──> Drop duplicates, handle nulls, merge title + text
         │
         ▼
[ NLP Preprocessing ]       ──> Lowercase, strip HTML/URLs, tokenize, remove stopwords, lemmatize
         │
         ▼
[ Exploratory Data Analysis] ──> Class distributions, article lengths, top word frequencies
         │
         ▼
[ Stratified Split (80/20) ] ──> 5,044 Train / 1,262 Test (random_state=42)
         │
         ▼
[ TF-IDF Feature Extraction] ──> Fitted strictly on Train set (Zero Data Leakage)
         │
         ├──────────────────────┬──────────────────────┐
         ▼                      ▼                      ▼
  [ Naive Bayes ]      [ Logistic Regression ]   [ Linear SVM ]
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                                ▼
                     [ Model Evaluation ]
                 (Accuracy, Precision, Recall, F1)
                                │
                                ▼
                 [ Dynamic Model Selection ]
                   (Winner: Linear SVM - F1: 0.9263)
                                │
                                ▼
                 [ Streamlit Web Application ]
```

---

## 8. Data Preprocessing
Implemented in `src/preprocessing.py`, the pipeline applies identical transformations during both batch training and real-time inference:
1. **Lowercasing:** Converts all text to uniform lowercase to avoid case-sensitive duplicate tokens.
2. **HTML Tag Stripping:** Removes formatting tags like `<p>`, `<a>`, and `<b>` using regex.
3. **URL & Link Removal:** Strips web links (`http://...`, `www...`).
4. **Special Character Filtering:** Removes non-alphabetic symbols while preserving word boundaries.
5. **Whitespace Normalization:** Collapses multiple spaces, tabs, and newlines into single spaces.
6. **Tokenization:** Breaks continuous text into individual word tokens.
7. **Stopword Removal:** Eliminates high-frequency grammatical words (e.g., *the*, *is*, *at*, *which*) using NLTK English stopwords.
8. **Lemmatization:** Reduces inflected word forms to their dictionary lemma (e.g., *running* $\rightarrow$ *run*, *better* $\rightarrow$ *good*) using `WordNetLemmatizer`.

---

## 9. Exploratory Data Analysis
EDA findings generated and saved inside `results/eda/`:
- **Class Balance (`class_distribution.png`):** Balanced dataset (50.02% REAL vs. 49.98% FAKE), preventing majority-class prediction bias.
- **Article Length (`article_length_distribution.png`):** REAL articles average **492.5 words**, while FAKE articles average **380.5 words**. Fabricated articles tend to exhibit shorter, sensationalized writeups.
- **Top Tokens (`top_words_real.png`, `top_words_fake.png`):** Captures high-frequency terms in both corpora for descriptive analysis.

---

## 10. TF-IDF Feature Extraction
- **Algorithm:** `sklearn.feature_extraction.text.TfidfVectorizer`
- **Configuration:**
  - `max_features=5000`: Captures the top 5,000 most informative unigram and bigram tokens.
  - `ngram_range=(1, 2)`: Includes single words and two-word phrases (e.g., *white house*, *breaking news*).
  - `min_df=3`: Filters out rare words and typos appearing in fewer than 3 articles.
  - `max_df=0.90`: Ignores corpus-wide ubiquitous words appearing in over 90% of documents.
  - `sublinear_tf=True`: Employs sublinear scaling ($1 + \log(\text{tf})$) to dampen the dominance of repetitive words.

> **CRITICAL DATA-LEAKAGE PREVENTION RULE:**  
> The TF-IDF vectorizer is **fitted strictly on the training set (`X_train`)**. The test set (`X_test`) is transformed using the pre-fitted vocabulary and IDF weights. Test data was never used in vocabulary creation or feature tuning.

---

## 11. Machine Learning Algorithms

### 1. Multinomial Naive Bayes (`MultinomialNB`)
- Grounded in Bayes' Theorem with conditional word independence assumptions:
  $$P(c|d) \propto P(c) \prod_{i=1}^n P(w_i|c)$$
- Uses Laplace smoothing ($\alpha=0.1$) to prevent zero-probability errors for unseen n-grams.

### 2. Logistic Regression (`LogisticRegression`)
- Fits a linear decision boundary mapped to probability space via the sigmoid activation:
  $$P(y=\text{REAL}|x) = \frac{1}{1 + e^{-(w^T x + b)}}$$
- Regularization $C=1.0$, optimized with L-BFGS solver over 1,000 maximum iterations.

### 3. Linear Support Vector Machine (`LinearSVC`)
- Determines the optimal maximum-margin hyperplane separating classes in high-dimensional TF-IDF space:
  $$\min_{w, b} \frac{1}{2} \|w\|^2 + C \sum_{i} \max(0, 1 - y_i(w^T x_i + b))$$
- Penalty parameter $C=1.0$, `dual="auto"`.

---

## 12. Model Evaluation
All models were evaluated on the exact same isolated test set (1,262 articles, 20% stratified split).

### Actual Test Set Results

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
|---|:---:|:---:|:---:|:---:|
| **Linear Support Vector Machine (Linear SVM)** | **92.63%** | **0.9263** | **0.9263** | **0.9263** |
| **Logistic Regression** | 91.44% | 0.9146 | 0.9144 | 0.9144 |
| **Multinomial Naive Bayes** | 87.72% | 0.8803 | 0.8772 | 0.8769 |

Individual classification reports and confusion matrices are saved in:
- `results/metrics/`
- `results/confusion_matrices/`

---

## 13. Model Selection
- **Selection Criterion:** Highest Macro F1-score on the isolated test set.
- **Winning Model:** **Linear Support Vector Machine (Linear SVM)**
- **Reason:** Linear SVM achieved an outstanding **92.63% test accuracy** and **0.9263 Macro F1-Score**, excelling at maximizing margins in high-dimensional sparse TF-IDF text representations.
- **Serialization:** Saved as `models/final_model.pkl` along with training metadata in `models/model_metadata.json`.

---

## 14. Streamlit Application
The project includes a clean academic Streamlit interface (`app.py`):
- Real-time text analysis of user-entered or pasted articles.
- One-click sample test buttons for quick viva demonstration.
- Prediction banner (**REAL NEWS** vs. **FAKE NEWS**) with Model Confidence percentage.
- Inspection expander displaying cleaned NLP tokens.
- Interactive tabs for:
  - Theoretical algorithm explanations (Viva notes).
  - Model comparison table and test confusion matrices.
  - Exploratory Data Analysis figures.
- Cached model loading via `@st.cache_resource` (no retraining on startup).

---

## 15. Project Structure

```
fake-news-detection/
├── data/
│   ├── raw/
│   │   └── fake_or_real_news.csv         # Raw benchmark dataset (6,335 rows)
│   └── processed/
│       └── cleaned_news.csv              # Cleaned dataset (6,306 rows)
├── models/
│   ├── tfidf_vectorizer.pkl              # Fitted TF-IDF vectorizer
│   ├── naive_bayes.pkl                   # Trained MultinomialNB
│   ├── logistic_regression.pkl           # Trained Logistic Regression
│   ├── linear_svm.pkl                    # Trained LinearSVC
│   ├── final_model.pkl                   # Selected best model (Linear SVM)
│   └── model_metadata.json               # Training config and evaluation metrics
├── notebooks/
│   └── fake_news_exploration.ipynb       # Jupyter notebook exploration
├── results/
│   ├── eda/
│   │   ├── class_distribution.png
│   │   ├── article_length_distribution.png
│   │   ├── top_words_real.png
│   │   └── top_words_fake.png
│   ├── confusion_matrices/
│   │   ├── naive_bayes_cm.png
│   │   ├── logistic_regression_cm.png
│   │   └── linear_svm_cm.png
│   └── metrics/
│       ├── model_comparison.csv
│       ├── naive_bayes_classification_report.txt
│       ├── logistic_regression_classification_report.txt
│       └── linear_svm_classification_report.txt
├── src/
│   ├── __init__.py
│   ├── data_loader.py                    # Dataset loading, validation, cleaning
│   ├── preprocessing.py                  # Text cleaning, tokenization, lemmatization
│   ├── feature_engineering.py            # Train/test split, TF-IDF vectorization
│   ├── train.py                          # Classical ML model training
│   ├── evaluate.py                       # Evaluation metrics, CM plots, model selection
│   └── predict.py                        # Standalone prediction pipeline and CLI
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py                  # Unit and integration test suite
├── app.py                                # Streamlit web application
├── requirements.txt                      # Project dependencies
├── README.md                             # Comprehensive documentation
├── .gitignore                            # Git ignore configuration
└── run_pipeline.py                       # Master end-to-end execution script
```

---

## 16. Installation

### 1. Clone the Repository:
```bash
git clone https://github.com/sunnykarthik15/ML-MINI-PROJECT.git
cd ML-MINI-PROJECT
```

### 2. Create a Virtual Environment:
```bash
python -m venv .venv
```

### 3. Activate the Environment:
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Dependencies:
```bash
pip install -r requirements.txt
```

---

## 17. Running the Project

### Execute the Full ML Pipeline:
Runs dataset loading, cleaning, NLP preprocessing, EDA generation, TF-IDF feature extraction, training 3 models, evaluation, and dynamic model selection:
```bash
python run_pipeline.py
```

### Run Automated Tests:
```bash
python -m unittest discover tests
```

### Run the Streamlit Web Application:
```bash
python -m streamlit run app.py
```
*(Or `streamlit run app.py`)*

---

## 18. Example Usage

### Via Command-Line Interface (CLI):
```bash
python src/predict.py --text "WASHINGTON (Reuters) - The U.S. House of Representatives passed comprehensive tax reform legislation on Tuesday, bringing the bill closer to the president's desk for signature."
```

**Output:**
```
==================================================
PREDICTION:       REAL
MODEL CONFIDENCE: 59.95% (Margin: +0.40)
SELECTED MODEL:   Linear SVM
==================================================
```

---

## 19. Limitations
1. **Linguistic Pattern Dependency:** The model learns stylistic, vocabulary, and lexical patterns from the training dataset. It classifies writing style, not external factual ground truth.
2. **Dataset Bias:** Historical political corpora influence the learned vocabulary; shifts in political figures, topical domains, or phrasing may impact accuracy.
3. **No External Verification:** The system does not query search engines or live knowledge graphs to verify real-world claims.
4. **Adversarial Text:** Fabricated articles carefully drafted in formal AP/Reuters journalistic style may mislead a classical bag-of-words classifier.
5. **Contextual Semantics:** TF-IDF n-grams capture local co-occurrences but lack full bidirectional sentence context.

---

## 20. Future Scope
- **Contextual Embeddings:** Integrating transformer architectures (e.g., BERT, RoBERTa) for deep semantic comprehension.
- **Multimodal Classification:** Combining text analysis with image forensics and metadata verification.
- **Retrieval-Augmented Fact Verification:** Pairing linguistic classification with automated evidence retrieval against trusted knowledge bases (e.g., Wikipedia, FactCheck.org).
- **Multilingual Support:** Extending detection to non-English languages and regional news sources.
- **Explainable AI (XAI):** Implementing SHAP or LIME token attribution to visually highlight which specific phrases triggered a FAKE classification.

---

## Viva & Defense FAQ Quick Reference

- **Q: Why did Linear SVM outperform Naive Bayes?**  
  *A:* In high-dimensional sparse TF-IDF spaces (5,000 features), classes are often linearly separable. Linear SVM finds the maximum-margin hyperplane, penalizing misclassifications while resisting overfitting. In contrast, Naive Bayes assumes strict conditional independence between words, which is violated in natural language.
- **Q: How did you ensure zero data leakage?**  
  *A:* Data was split into 80% train and 20% test before feature engineering. The `TfidfVectorizer` was fitted strictly on `X_train`. The test set was merely transformed with the pre-fitted vectorizer.
- **Q: What is the significance of sublinear TF?**  
  *A:* It replaces term frequency $\text{tf}$ with $1 + \log(\text{tf})$, preventing articles that mention a word twenty times from dominating articles that mention it twice.