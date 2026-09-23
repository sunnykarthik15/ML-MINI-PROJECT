"""
Academic Mini-Project Word Document (.docx) Generator for BTech CSE.
Generates an editable Word report complete with all 10 chapters,
embedded figures, tables, code snippets, and references.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_border(cell, **kwargs):
    """Set cell borders for docx tables."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'CBD5E1'))
            tcBorders.append(element)
    tcPr.append(tcBorders)


def create_docx_report(output_docx_path="reports/Fake_News_Detection_Project_Report.docx"):
    os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Helper styling functions
    def add_custom_heading(text, level, color=RGBColor(30, 58, 138)):
        h = doc.add_heading(text, level=level)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        run = h.runs[0]
        run.font.color.rgb = color
        run.font.name = "Calibri"
        return h

    def add_body_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(10.5)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(text)
        r.italic = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(100, 116, 139)
        return p

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pre = p_pre.add_run("A MINI-PROJECT REPORT ON")
    r_pre.font.size = Pt(11)
    r_pre.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("FAKE NEWS DETECTION USING NATURAL LANGUAGE PROCESSING AND MACHINE LEARNING")
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("An Explainable Classical NLP and Machine Learning Classification System")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(20)
    r_deg = p_deg.add_run("Submitted in partial fulfillment of the requirements for the award of the degree of\n")
    r_deg.italic = True
    r_deg.font.size = Pt(10)
    r_deg2 = p_deg.add_run("BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING\n")
    r_deg2.bold = True
    r_deg2.font.size = Pt(12)
    r_deg2.font.color.rgb = RGBColor(30, 58, 138)

    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.rows[0].cells[0].paragraphs[0].add_run("Submitted By:").bold = True
    meta_table.rows[0].cells[1].paragraphs[0].add_run("Under the Guidance of:").bold = True
    meta_table.rows[1].cells[0].paragraphs[0].add_run("Student Name: G. Karthik\nRoll: BTech CSE Final Year\nDept of Computer Science & Engg.")
    meta_table.rows[1].cells[1].paragraphs[0].add_run("Department Project Coordinator\nDept of Computer Science & Engg.\nAcademic Year: 2025 – 2026")

    doc.add_page_break()

    # =========================================================================
    # CERTIFICATE & DECLARATION
    # =========================================================================
    add_custom_heading("CERTIFICATE OF AUTHENTICITY", level=1)
    add_body_p(
        "This is to certify that the mini-project report entitled \"Fake News Detection Using Natural Language Processing and Machine Learning\" "
        "is a bonafide work carried out by G. Karthik in partial fulfillment of the requirements for the award of the degree of "
        "Bachelor of Technology in Computer Science and Engineering during the academic year 2025–2026."
    )
    add_body_p(
        "The project demonstrates genuine technical rigor, zero data-leakage during feature extraction, classical machine learning evaluation, "
        "and interactive deployment. To the best of our knowledge, the results incorporated in this report are authentic and obtained through actual execution."
    )

    cert_tbl = doc.add_table(rows=1, cols=3)
    cert_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cert_tbl.rows[0].cells[0].paragraphs[0].add_run("\n\nInternal Guide / Supervisor\nDept of CSE")
    cert_tbl.rows[0].cells[1].paragraphs[0].add_run("\n\nHead of the Department\nDept of CSE")
    cert_tbl.rows[0].cells[2].paragraphs[0].add_run("\n\nExternal Examiner\nViva-Voce Examination")

    add_custom_heading("CANDIDATE'S DECLARATION", level=1)
    add_body_p(
        "I hereby declare that the work presented in this project report entitled \"Fake News Detection Using Natural Language Processing and Machine Learning\" "
        "is an authentic record of my own work carried out under guidance. I have not submitted the matter embodied in this report for the award of any other degree or diploma."
    )
    add_body_p("Date: 23rd September 2026\nPlace: Campus\n\n(G. Karthik)\nSignature of the Candidate")

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT & TOC
    # =========================================================================
    add_custom_heading("ABSTRACT", level=1)
    add_body_p(
        "The unchecked spread of fabricated news articles across online ecosystems presents severe challenges to democratic discourse, "
        "financial markets, and public health. This project designs and implements an academic, interpretable machine learning system for binary news "
        "classification (REAL vs. FAKE) using classical Natural Language Processing (NLP) techniques and statistical classifiers. "
        "Utilizing a verified benchmark dataset of 6,335 articles, comprehensive data cleaning and deduplication produced 6,306 normalized records with "
        "a balanced distribution (3,154 REAL, 3,152 FAKE). A leak-free NLP pipeline cleans, tokenizes, removes stopwords, and lemmatizes raw news text."
    )
    add_body_p(
        "Numerical features were extracted using Term Frequency-Inverse Document Frequency (TF-IDF) fitted strictly on training data (5,044 samples). "
        "Three classical algorithms—Multinomial Naive Bayes, Logistic Regression, and Linear Support Vector Machine (Linear SVM)—were "
        "trained and systematically evaluated on an isolated held-out test set (1,262 samples). Linear SVM demonstrated superior performance, "
        "achieving an accuracy of 92.63% and a Macro F1-score of 0.9263. A streamlined Streamlit web application demonstrates real-time inference, "
        "confidence estimation, preprocessed token inspection, and model explainability without external APIs or deep learning black-boxes."
    )

    add_custom_heading("TABLE OF CONTENTS", level=1)
    toc_items = [
        ("1", "Introduction and Problem Definition", "4"),
        ("2", "Literature Survey and Related Work", "5"),
        ("3", "System Architecture & Requirements", "6"),
        ("4", "Dataset Acquisition and Exploratory Data Analysis (EDA)", "7"),
        ("5", "NLP Preprocessing & Feature Engineering", "9"),
        ("6", "Machine Learning Algorithms & Mathematical Foundations", "11"),
        ("7", "Experimental Results and Comparative Model Evaluation", "13"),
        ("8", "Interactive Web Application & System Demonstration", "15"),
        ("9", "Critical Analysis, Limitations & Ethical Considerations", "18"),
        ("10", "Conclusion & Future Scope", "19"),
        ("—", "References, Bibliography & Appendix Execution Guide", "20"),
    ]
    t_toc = doc.add_table(rows=1, cols=3)
    t_toc.rows[0].cells[0].paragraphs[0].add_run("Chapter").bold = True
    t_toc.rows[0].cells[1].paragraphs[0].add_run("Title").bold = True
    t_toc.rows[0].cells[2].paragraphs[0].add_run("Page").bold = True
    for ch, ti, pg in toc_items:
        row = t_toc.add_row()
        row.cells[0].paragraphs[0].add_run(ch)
        row.cells[1].paragraphs[0].add_run(ti)
        row.cells[2].paragraphs[0].add_run(pg)

    doc.add_page_break()

    # =========================================================================
    # CHAPTERS 1 TO 3
    # =========================================================================
    add_custom_heading("CHAPTER 1: INTRODUCTION", level=1)
    add_custom_heading("1.1 Background & Context", level=2)
    add_body_p(
        "In modern digital society, information dissemination has transitioned from centralized legacy broadcasting networks to decentralized, "
        "algorithmic social feeds, messaging groups, and online publishing portals. While this democratizes free expression and enables instantaneous reporting, "
        "it also facilitates the viral spread of deceptive, sensationalist, or entirely fabricated news stories. Fabricated news—commonly termed 'Fake News'—refers "
        "to intentionally published falsehoods designed to deceive readers for political propaganda, ideological manipulation, or ad-revenue maximization through clickbait."
    )
    add_body_p(
        "Manual verification by professional fact-checkers is inherently unscalable given the tens of thousands of articles published every minute. "
        "Consequently, automated text classification systems grounded in Computer Science and Machine Learning have become an imperative area of research."
    )
    add_custom_heading("1.2 Problem Definition", level=2)
    add_body_p(
        "Mathematically, the problem is formulated as a supervised binary text classification task. Let D = {(x1, y1), (x2, y2), ..., (xn, yn)} "
        "denote a training corpus where each document xi in X is an unstructured textual sequence comprising a news headline and article body, "
        "and yi in {REAL, FAKE} represents the ground-truth authenticity label. The objective is to learn an optimal classification function "
        "f: X -> {REAL, FAKE} that maximizes generalization accuracy and Macro F1-score on previously unseen test documents while guaranteeing zero data leakage."
    )
    add_custom_heading("1.3 Objectives of the Project", level=2)
    add_body_p("1. Build an automated modular pipeline executing data loading, cleaning, NLP preprocessing, EDA, feature extraction, training, evaluation, and inference.", bold_prefix="• ")
    add_body_p("2. Employ explainable classical NLP techniques (lowercasing, stopword filtering, WordNet lemmatization, and TF-IDF) without opaque deep neural networks.", bold_prefix="• ")
    add_body_p("3. Implement, tune, and comparatively evaluate three prominent algorithms: Multinomial Naive Bayes, Logistic Regression, and Linear Support Vector Machines.", bold_prefix="• ")
    add_body_p("4. Select the superior model based strictly on empirical Macro F1 performance on an isolated held-out test set.", bold_prefix="• ")
    add_body_p("5. Develop a lightweight, responsive Streamlit application for real-time demonstration with confidence metrics and viva explanation notes.", bold_prefix="• ")

    doc.add_page_break()

    # CHAPTER 2
    add_custom_heading("CHAPTER 2: LITERATURE SURVEY & RELATED WORK", level=1)
    add_custom_heading("2.1 Evolution of Fake News Detection Methodologies", level=2)
    add_body_p(
        "Automated detection of deceptive text originated in computational linguistics and sentiment analysis. Early approaches by Mihalcea et al. (2009) "
        "and Rubin et al. (2015) established that deceptive writing styles exhibit quantifiable lexical, syntactic, and semantic regularities. "
        "Fabricated articles frequently deploy elevated rates of sensationalist adjectives, informal punctuation, exclamation marks, and exaggerated claims, "
        "contrasting with traditional journalistic reporting which adheres to neutral, passive-voice constructs and formal institutional terminology."
    )
    add_custom_heading("2.2 Classical NLP vs. Modern Deep Learning", level=2)
    add_body_p(
        "While deep learning models (BERT, RoBERTa) achieve impressive results, classical machine learning offers decisive pedagogical and engineering advantages "
        "for academic mini-projects: near-zero computational latency (<25ms inference), total transparency of learned feature weights, resilience against overfitting "
        "on moderate datasets, and complete independence from costly external APIs or heavy GPU infrastructures."
    )

    doc.add_page_break()

    # CHAPTER 3
    add_custom_heading("CHAPTER 3: SYSTEM ARCHITECTURE & REQUIREMENTS", level=1)
    add_custom_heading("3.1 High-Level Pipeline Architecture", level=2)
    add_body_p(
        "The system follows a strict, sequential seven-stage architectural pipeline designed for modularity, maintainability, and total reproducibility: "
        "1. Raw Ingestion -> 2. Data Cleaning & Deduplication -> 3. NLP Preprocessing -> 4. Exploratory Data Analysis -> 5. Stratified Split & TF-IDF Extraction -> "
        "6. Classical ML Model Training -> 7. Evaluation & Dynamic Model Selection -> 8. Streamlit Web Deployment."
    )
    add_custom_heading("3.2 Hardware and Software Environment", level=2)
    add_body_p("Python 3.11.x 64-bit; Scikit-learn (1.3+), Pandas (2.0+), NumPy (1.24+), NLTK (3.8+), Matplotlib (3.7+), Seaborn (0.12+), Streamlit (1.30+), Joblib (1.3+).", bold_prefix="Software: ")
    add_body_p("Standard Dual/Quad Core CPU, 4 GB RAM minimum (8 GB recommended), 500 MB free storage.", bold_prefix="Hardware: ")

    doc.add_page_break()

    # CHAPTER 4: DATASET & EDA
    add_custom_heading("CHAPTER 4: DATASET & EXPLORATORY DATA ANALYSIS", level=1)
    add_custom_heading("4.1 Dataset Acquisition and Cleaning", level=2)
    add_body_p(
        "The project utilizes the authentic benchmark dataset (George McIntire & Katharine Jarmul) containing 6,335 initial records. "
        "Deduplication removed 29 duplicate articles, producing 6,306 normalized records with a balanced distribution (3,154 REAL, 3,152 FAKE)."
    )

    if os.path.exists("results/eda/class_distribution.png"):
        doc.add_picture("results/eda/class_distribution.png", width=Inches(5.5))
        add_caption("Figure 4.1: Class Distribution of Cleaned News Dataset (50.02% REAL vs. 49.98% FAKE).")

    add_custom_heading("4.2 Article Length and Word Frequency Distributions", level=2)
    add_body_p(
        "REAL news articles averaged 492.5 words, displaying characteristic depth and cited attribution, while FAKE articles averaged 380.5 words, "
        "characterized by concise sensationalist phrasing."
    )

    if os.path.exists("results/eda/article_length_distribution.png"):
        doc.add_picture("results/eda/article_length_distribution.png", width=Inches(5.5))
        add_caption("Figure 4.2: Article Word Count Distribution across REAL and FAKE categories.")

    doc.add_page_break()

    # Top Words EDA
    add_custom_heading("4.3 Top Word Frequency Distributions", level=2)
    if os.path.exists("results/eda/top_words_real.png"):
        doc.add_picture("results/eda/top_words_real.png", width=Inches(5.0))
        add_caption("Figure 4.3: Top 20 Most Frequent Lemmatized Tokens in REAL News.")
    if os.path.exists("results/eda/top_words_fake.png"):
        doc.add_picture("results/eda/top_words_fake.png", width=Inches(5.0))
        add_caption("Figure 4.4: Top 20 Most Frequent Lemmatized Tokens in FAKE News.")

    doc.add_page_break()

    # CHAPTER 5: NLP PREPROCESSING & TF-IDF
    add_custom_heading("CHAPTER 5: NLP PREPROCESSING & FEATURE ENGINEERING", level=1)
    add_custom_heading("5.1 Preprocessing Pipeline", level=2)
    add_body_p(
        "The text preprocessing pipeline in src/preprocessing.py executes: 1. Lowercasing; 2. HTML tag stripping; 3. URL and link removal; "
        "4. Non-alphabetic character filtering; 5. Whitespace normalization; 6. NLTK tokenization; 7. Stopword removal; 8. WordNet lemmatization."
    )
    add_custom_heading("5.2 TF-IDF and Zero Data Leakage Protocol", level=2)
    add_body_p(
        "Features are extracted using TfidfVectorizer (5,000 features, unigrams and bigrams, sublinear_tf=True). "
        "To ensure zero data leakage, the vectorizer is strictly fitted ONLY on X_train (5,044 samples). The test set (1,262 samples) "
        "is transformed using the pre-fitted vocabulary."
    )

    doc.add_page_break()

    # CHAPTER 6 & 7: MODELS & RESULTS
    add_custom_heading("CHAPTER 6 & 7: MACHINE LEARNING MODELS & EVALUATION", level=1)
    add_custom_heading("6.1 Algorithms Evaluated", level=2)
    add_body_p("Multinomial Naive Bayes (alpha=0.1), Logistic Regression (C=1.0, max_iter=1000), and Linear Support Vector Machine (LinearSVC, C=1.0).")

    add_custom_heading("7.1 Comparative Results on Test Set (1,262 Articles)", level=2)
    res_tbl = doc.add_table(rows=1, cols=5)
    res_tbl.rows[0].cells[0].paragraphs[0].add_run("Model").bold = True
    res_tbl.rows[0].cells[1].paragraphs[0].add_run("Accuracy").bold = True
    res_tbl.rows[0].cells[2].paragraphs[0].add_run("Precision").bold = True
    res_tbl.rows[0].cells[3].paragraphs[0].add_run("Recall").bold = True
    res_tbl.rows[0].cells[4].paragraphs[0].add_run("Macro F1").bold = True

    model_rows = [
        ("Linear Support Vector Machine (Linear SVM)", "92.63%", "0.9263", "0.9263", "0.9263"),
        ("Logistic Regression", "91.44%", "0.9146", "0.9144", "0.9144"),
        ("Multinomial Naive Bayes", "87.72%", "0.8803", "0.8772", "0.8769"),
    ]
    for m, a, p, r, f in model_rows:
        row = res_tbl.add_row()
        row.cells[0].paragraphs[0].add_run(m)
        row.cells[1].paragraphs[0].add_run(a)
        row.cells[2].paragraphs[0].add_run(p)
        row.cells[3].paragraphs[0].add_run(r)
        row.cells[4].paragraphs[0].add_run(f)

    add_body_p(
        "\nWinner: Linear SVM achieved peak performance with 92.63% accuracy and 0.9263 Macro F1-score, "
        "dynamically selected and saved as models/final_model.pkl."
    )

    if os.path.exists("results/confusion_matrices/linear_svm_cm.png"):
        doc.add_picture("results/confusion_matrices/linear_svm_cm.png", width=Inches(4.5))
        add_caption("Figure 7.1: Confusion Matrix for Winning Linear SVM Model.")

    doc.add_page_break()

    # CHAPTER 8: STREAMLIT APPLICATION & SCREENSHOTS
    add_custom_heading("CHAPTER 8: INTERACTIVE WEB APPLICATION & DEMONSTRATION", level=1)
    add_custom_heading("8.1 System Interface & Viva Demonstration", level=2)
    add_body_p(
        "The Streamlit application (app.py) provides non-technical examiners with a clean, responsive interface featuring "
        "one-click sample buttons, real-time inference, confidence meters, token inspection, and interactive evaluation tabs."
    )

    if os.path.exists("reports/screenshots/01_streamlit_home.png"):
        doc.add_picture("reports/screenshots/01_streamlit_home.png", width=Inches(5.5))
        add_caption("Figure 8.1: Streamlit Web Application Homepage.")

    if os.path.exists("reports/screenshots/02_real_news_prediction.png"):
        doc.add_picture("reports/screenshots/02_real_news_prediction.png", width=Inches(5.5))
        add_caption("Figure 8.2: Real News Article Classification with Green Status Banner.")

    doc.add_page_break()

    if os.path.exists("reports/screenshots/03_fake_news_prediction.png"):
        doc.add_picture("reports/screenshots/03_fake_news_prediction.png", width=Inches(5.5))
        add_caption("Figure 8.3: Fake News Article Classification with Red Status Banner.")

    if os.path.exists("reports/screenshots/05_model_comparison_and_cm.png"):
        doc.add_picture("reports/screenshots/05_model_comparison_and_cm.png", width=Inches(5.5))
        add_caption("Figure 8.4: Interactive Model Comparison & Confusion Matrix Tab.")

    doc.add_page_break()

    # CHAPTER 9 & 10: LIMITATIONS, CONCLUSION, REFERENCES
    add_custom_heading("CHAPTER 9: CRITICAL ANALYSIS & LIMITATIONS", level=1)
    add_body_p("1. Style vs. Factuality: The model classifies linguistic and stylistic patterns, not physical ground truth.", bold_prefix="• ")
    add_body_p("2. Temporal Drift: Historical datasets may experience performance degradation on future geopolitical terminology.", bold_prefix="• ")
    add_body_p("3. Adversarial Text: Intentionally crafted falsehoods formatted in formal AP style may evade detection.", bold_prefix="• ")

    add_custom_heading("CHAPTER 10: CONCLUSION & FUTURE SCOPE", level=1)
    add_body_p(
        "This project successfully engineered an explainable, leak-free classical NLP fake news detection system. "
        "Linear SVM achieved 92.63% test accuracy and 0.9263 Macro F1, providing an exemplary academic mini-project. "
        "Future enhancements could include contextual transformer embeddings (BERT), retrieval-augmented fact verification, and multimodal image forensics."
    )

    add_custom_heading("REFERENCES & APPENDIX", level=1)
    add_body_p("[1] V. L. Rubin et al., 'Deception detection for news: three types of fakes,' Proc. ASIS&T, 2015.")
    add_body_p("[2] K. Shu et al., 'Fake news detection on social media: A data mining perspective,' ACM SIGKDD, 2017.")
    add_body_p("[3] G. McIntire and K. Jarmul, 'Fake and real news dataset,' DataCamp Tutorial, 2016.")
    add_body_p("[4] F. Pedregosa et al., 'Scikit-learn: Machine learning in Python,' JMLR, 2011.")
    add_body_p("\nGitHub Repository: https://github.com/sunnykarthik15/ML-MINI-PROJECT")

    doc.save(output_docx_path)
    print(f"[DOCX Generator] Successfully generated: '{output_docx_path}'")


if __name__ == "__main__":
    create_docx_report()
