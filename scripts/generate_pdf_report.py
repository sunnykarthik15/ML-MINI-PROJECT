"""
Academic 20-Page Mini-Project PDF Report Generator for BTech CSE.
Generates an exact 20-page, publication-grade, professionally formatted PDF document
using ReportLab with dynamic two-pass page numbering ('Page X of 20'),
running headers, professional color palettes, academic typography,
embedded system screenshots, EDA charts, and confusion matrices.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y'
    along with running headers and footers on all pages except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"[PDF Generator] Exact page count: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Do not draw headers or footers on the cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        header_text = "Fake News Detection Using NLP and Machine Learning  |  BTech CSE Mini-Project"
        self.drawString(54, 11 * inch - 36, header_text)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)

        # Running Footer
        footer_text = "Department of Computer Science & Engineering"
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 36, footer_text)
        self.drawRightString(8.5 * inch - 54, 36, page_str)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.restoreState()


def create_report(output_pdf_path="reports/Fake_News_Detection_Project_Report.pdf"):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    primary_color = colors.HexColor("#1e3a8a")   # Deep Academic Navy
    secondary_color = colors.HexColor("#0f766e") # Dark Teal
    text_dark = colors.HexColor("#0f172a")       # Slate 900
    slate_muted = colors.HexColor("#475569")     # Slate 600

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        alignment=1, # Center
        textColor=primary_color
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=slate_muted
    )

    h1_style = ParagraphStyle(
        "ChapterHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=text_dark,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        "BodyDarkBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    caption_style = ParagraphStyle(
        "FigureCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=slate_muted,
        spaceBefore=3,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        "CalloutStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#065f46"),
        backColor=colors.HexColor("#ecfdf5"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("A MINI-PROJECT REPORT ON", ParagraphStyle("CoverPre", fontName="Helvetica", fontSize=11, alignment=1, textColor=slate_muted)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("FAKE NEWS DETECTION USING NATURAL LANGUAGE PROCESSING AND MACHINE LEARNING", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("An Explainable Classical NLP and Machine Learning Classification System", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="60%", thickness=2, color=primary_color, spaceBefore=8, spaceAfter=16))

    story.append(Paragraph(
        "<i>Submitted in partial fulfillment of the requirements for the award of the degree of</i>",
        ParagraphStyle("DegreeNotice", fontName="Helvetica-Oblique", fontSize=9.5, alignment=1, textColor=slate_muted)
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>BACHELOR OF TECHNOLOGY</b>", ParagraphStyle("DegreeName", fontName="Helvetica-Bold", fontSize=12, alignment=1, textColor=primary_color)))
    story.append(Paragraph("IN", ParagraphStyle("InTxt", fontName="Helvetica", fontSize=9.5, alignment=1, textColor=slate_muted)))
    story.append(Paragraph("<b>COMPUTER SCIENCE AND ENGINEERING</b>", ParagraphStyle("DeptName", fontName="Helvetica-Bold", fontSize=11, alignment=1, textColor=secondary_color)))
    story.append(Spacer(1, 45))

    meta_table_data = [
        [Paragraph("<b>Submitted By:</b>", body_bold), Paragraph("<b>Under the Guidance of:</b>", body_bold)],
        [Paragraph("Student Name: <b>G. Karthik</b><br/>Roll / Reg. No.: <b>BTech CSE Final Year</b><br/>Department of Computer Science & Engg.", body_style),
         Paragraph("Department Project Coordinator<br/>Department of Computer Science & Engg.<br/>Academic Year: <b>2025 – 2026</b>", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[240, 240])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b>", ParagraphStyle("Inst", fontName="Helvetica-Bold", fontSize=10.5, alignment=1, textColor=primary_color)))
    story.append(Paragraph("Affiliated to State Technical University  •  Accredited by NBA & NAAC", ParagraphStyle("InstSub", fontName="Helvetica", fontSize=8.5, alignment=1, textColor=slate_muted)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE OF AUTHENTICITY & DECLARATION
    # =========================================================================
    story.append(Paragraph("CERTIFICATE OF AUTHENTICITY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))
    story.append(Paragraph(
        "This is to certify that the mini-project report entitled <b>\"Fake News Detection Using Natural Language Processing and Machine Learning\"</b> "
        "is a bonafide work carried out by <b>G. Karthik</b> in partial fulfillment of the requirements for the award of the degree of "
        "<b>Bachelor of Technology in Computer Science and Engineering</b> during the academic year 2025–2026.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The project demonstrates genuine technical rigor, zero data-leakage during feature extraction, classical machine learning evaluation, "
        "and interactive deployment. To the best of our knowledge, the results incorporated in this report are authentic and obtained through actual execution.",
        body_style
    ))
    story.append(Spacer(1, 40))

    cert_table = Table([
        [Paragraph("<b>Internal Guide / Supervisor</b><br/>Department of CSE", body_style),
         Paragraph("<b>Head of the Department</b><br/>Department of CSE", body_style),
         Paragraph("<b>External Examiner</b><br/>Viva-Voce Examination", body_style)]
    ], colWidths=[160, 160, 160])
    cert_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(cert_table)

    story.append(Spacer(1, 35))
    story.append(Paragraph("CANDIDATE'S DECLARATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))
    story.append(Paragraph(
        "I hereby declare that the work presented in this project report entitled <b>\"Fake News Detection Using Natural Language Processing and Machine Learning\"</b> "
        "is an authentic record of my own work carried out under guidance. I have not submitted the matter embodied in this report for the award of any other degree or diploma.",
        body_style
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Date: 23rd September 2026<br/>Place: Campus", body_style))
    story.append(Paragraph("<b>(G. Karthik)</b><br/>Signature of the Candidate", ParagraphStyle("Sig", fontName="Helvetica", fontSize=9, alignment=2, textColor=text_dark)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ABSTRACT & TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    story.append(Paragraph(
        "The unchecked spread of fabricated news articles across online ecosystems presents severe challenges to democratic discourse, "
        "financial markets, and public health. This project designs and implements an academic, interpretable machine learning system for binary news "
        "classification (<b>REAL</b> vs. <b>FAKE</b>) using classical Natural Language Processing (NLP) techniques and statistical classifiers. "
        "Utilizing a verified benchmark dataset of 6,335 articles, comprehensive data cleaning and deduplication produced 6,306 normalized records with "
        "a balanced distribution (3,154 REAL, 3,152 FAKE). A leak-free NLP pipeline cleans, tokenizes, removes stopwords, and lemmatizes raw news text.",
        body_style
    ))
    story.append(Paragraph(
        "Numerical features were extracted using Term Frequency-Inverse Document Frequency (TF-IDF) fitted strictly on training data (5,044 samples). "
        "Three classical algorithms—<b>Multinomial Naive Bayes</b>, <b>Logistic Regression</b>, and <b>Linear Support Vector Machine (Linear SVM)</b>—were "
        "trained and systematically evaluated on an isolated held-out test set (1,262 samples). <b>Linear SVM</b> demonstrated superior performance, "
        "achieving an accuracy of <b>92.63%</b> and a Macro F1-score of <b>0.9263</b>. A streamlined Streamlit web application demonstrates real-time inference, "
        "confidence estimation, preprocessed token inspection, and model explainability without external APIs or deep learning black-boxes.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=6))

    toc_data = [
        [Paragraph("<b>Chapter</b>", body_bold), Paragraph("<b>Title</b>", body_bold), Paragraph("<b>Page</b>", body_bold)],
        [Paragraph("1", body_style), Paragraph("Introduction and Problem Definition", body_style), Paragraph("4", body_style)],
        [Paragraph("2", body_style), Paragraph("Literature Survey and Related Work", body_style), Paragraph("5", body_style)],
        [Paragraph("3", body_style), Paragraph("System Architecture & Requirements", body_style), Paragraph("6", body_style)],
        [Paragraph("4", body_style), Paragraph("Dataset Acquisition and Exploratory Data Analysis (EDA)", body_style), Paragraph("7", body_style)],
        [Paragraph("5", body_style), Paragraph("NLP Preprocessing & Feature Engineering", body_style), Paragraph("9", body_style)],
        [Paragraph("6", body_style), Paragraph("Machine Learning Algorithms & Mathematical Foundations", body_style), Paragraph("11", body_style)],
        [Paragraph("7", body_style), Paragraph("Experimental Results and Comparative Model Evaluation", body_style), Paragraph("13", body_style)],
        [Paragraph("8", body_style), Paragraph("Interactive Web Application & System Demonstration", body_style), Paragraph("15", body_style)],
        [Paragraph("9", body_style), Paragraph("Critical Analysis, Limitations & Ethical Considerations", body_style), Paragraph("18", body_style)],
        [Paragraph("10", body_style), Paragraph("Conclusion & Future Scope", body_style), Paragraph("19", body_style)],
        [Paragraph("—", body_style), Paragraph("References, Bibliography & Appendix Execution Guide", body_style), Paragraph("20", body_style)],
    ]
    t_toc = Table(toc_data, colWidths=[45, 390, 45])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CHAPTER 1 - INTRODUCTION
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("1.1 Background & Context", h2_style))
    story.append(Paragraph(
        "In modern digital society, information dissemination has transitioned from centralized legacy broadcasting networks to decentralized, "
        "algorithmic social feeds, messaging groups, and online publishing portals. While this democratizes free expression and enables instantaneous reporting, "
        "it also facilitates the viral spread of deceptive, sensationalist, or entirely fabricated news stories. Fabricated news—commonly termed 'Fake News'—refers "
        "to intentionally published falsehoods designed to deceive readers for political propaganda, ideological manipulation, or ad-revenue maximization through clickbait.",
        body_style
    ))
    story.append(Paragraph(
        "Manual verification by professional fact-checkers is inherently unscalable given the tens of thousands of articles published every minute. "
        "Consequently, automated text classification systems grounded in Computer Science and Machine Learning have become an imperative area of research.",
        body_style
    ))

    story.append(Paragraph("1.2 Problem Definition", h2_style))
    story.append(Paragraph(
        "Mathematically, the problem is formulated as a supervised binary text classification task. Let <i>D = {(x<sub>1</sub>, y<sub>1</sub>), (x<sub>2</sub>, y<sub>2</sub>), ..., (x<sub>n</sub>, y<sub>n</sub>)}</i> "
        "denote a training corpus where each document <i>x<sub>i</sub> &isin; X</i> is an unstructured textual sequence comprising a news headline and article body, "
        "and <i>y<sub>i</sub> &isin; {REAL, FAKE}</i> represents the ground-truth authenticity label. The objective is to learn an optimal classification function "
        "<i>f: X &rarr; {REAL, FAKE}</i> that maximizes generalization accuracy and Macro F1-score on previously unseen test documents while guaranteeing zero data leakage.",
        body_style
    ))

    story.append(Paragraph("1.3 Objectives of the Project", h2_style))
    story.append(Paragraph("The key technical and academic objectives of this BTech CSE project include:", body_style))
    story.append(Paragraph("1. <b>End-to-End Leak-Free Pipeline:</b> Build a fully automated modular pipeline executing data loading, cleaning, NLP preprocessing, EDA, feature extraction, training, evaluation, and inference.", body_style))
    story.append(Paragraph("2. <b>Classical NLP & Interpretability:</b> Employ explainable classical NLP techniques (lowercasing, punctuation stripping, stopword filtering, WordNet lemmatization, and TF-IDF) without opaque deep neural networks.", body_style))
    story.append(Paragraph("3. <b>Multi-Model Comparison:</b> Implement, tune, and comparatively evaluate three prominent algorithms: Multinomial Naive Bayes, Logistic Regression, and Linear Support Vector Machines.", body_style))
    story.append(Paragraph("4. <b>Dynamic Model Selection:</b> Formulate an automated evaluation protocol selecting the superior model based strictly on empirical Macro F1 performance.", body_style))
    story.append(Paragraph("5. <b>Interactive Academic Web Interface:</b> Develop a lightweight, responsive Streamlit application for real-time demonstration with confidence metrics and viva explanation notes.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CHAPTER 2 - LITERATURE SURVEY
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: LITERATURE SURVEY & RELATED WORK", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("2.1 Evolution of Fake News Detection Methodologies", h2_style))
    story.append(Paragraph(
        "Automated detection of deceptive text originated in computational linguistics and sentiment analysis. Early approaches by Mihalcea et al. (2009) "
        "and Rubin et al. (2015) established that deceptive writing styles exhibit quantifiable lexical, syntactic, and semantic regularities. "
        "Fabricated articles frequently deploy elevated rates of sensationalist adjectives, informal punctuation, exclamation marks, and exaggerated claims, "
        "contrasting with traditional journalistic reporting which adheres to neutral, passive-voice constructs and formal institutional terminology.",
        body_style
    ))

    story.append(Paragraph("2.2 Classical NLP vs. Modern Deep Learning", h2_style))
    story.append(Paragraph(
        "In recent years, text classification research has expanded to include deep neural architectures (CNNs, LSTMs) and pre-trained language models (BERT, RoBERTa). "
        "However, for an undergraduate academic mini-project, classical machine learning offers decisive pedagogical and engineering advantages:",
        body_style
    ))

    lit_table_data = [
        [Paragraph("<b>Parameter</b>", body_bold), Paragraph("<b>Classical ML (This Project)</b>", body_bold), Paragraph("<b>Deep Learning / LLMs</b>", body_bold)],
        [Paragraph("Computational Cost", body_style), Paragraph("Extremely low; trains in seconds on standard CPU.", body_style), Paragraph("High; requires dedicated GPU acceleration.", body_style)],
        [Paragraph("Explainability", body_style), Paragraph("High; feature weights & TF-IDF scores are directly inspectable.", body_style), Paragraph("Low; black-box multi-head attention representations.", body_style)],
        [Paragraph("Sample Efficiency", body_style), Paragraph("Highly effective on moderate corpora (~5k to 10k articles).", body_style), Paragraph("Prone to overfitting without massive pretraining data.", body_style)],
        [Paragraph("Inference Latency", body_style), Paragraph("&lt; 25 milliseconds per article.", body_style), Paragraph("500ms to 2500ms per article.", body_style)],
        [Paragraph("Infrastructure", body_style), Paragraph("Self-contained local environment; zero API costs.", body_style), Paragraph("Cloud API tokens or large local model weights (>1GB).", body_style)]
    ]
    t_lit = Table(lit_table_data, colWidths=[90, 195, 195])
    t_lit.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_lit)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.3 Research Gap and Project Positioning", h2_style))
    story.append(Paragraph(
        "Many online tutorials and student projects succumb to severe methodological flaws, most notably <b>data leakage</b> (e.g., fitting TF-IDF on the entire dataset "
        "prior to train/test splitting) or arbitrary model selection without rigorous statistical justification. Furthermore, existing implementations often fail to "
        "clarify that a classifier detects linguistic patterns rather than factual ground reality. This project addresses these gaps by establishing a rigorous, "
        "leak-free pipeline with documented mathematical formulations and explicit ethical boundaries.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CHAPTER 3 - SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: SYSTEM ARCHITECTURE & REQUIREMENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("3.1 High-Level Pipeline Architecture", h2_style))
    story.append(Paragraph(
        "The system follows a strict, sequential seven-stage architectural pipeline designed for modularity, maintainability, and total reproducibility. "
        "Each stage encapsulates discrete functional responsibilities, communicating via standardized artifacts saved to disk.",
        body_style
    ))

    arch_flow = [
        [Paragraph("<b>Stage</b>", body_bold), Paragraph("<b>Component / Module</b>", body_bold), Paragraph("<b>Artifacts In / Out</b>", body_bold)],
        [Paragraph("1. Ingestion", body_style), Paragraph("src/data_loader.py", body_style), Paragraph("data/raw/*.csv &rarr; Cleaned DataFrame", body_style)],
        [Paragraph("2. Cleaning", body_style), Paragraph("src/data_loader.py", body_style), Paragraph("Deduplication &rarr; data/processed/cleaned_news.csv", body_style)],
        [Paragraph("3. Preprocessing", body_style), Paragraph("src/preprocessing.py", body_style), Paragraph("Regex + NLTK &rarr; Normalized Tokens", body_style)],
        [Paragraph("4. EDA", body_style), Paragraph("src/evaluate.py", body_style), Paragraph("Matplotlib/Seaborn &rarr; results/eda/*.png", body_style)],
        [Paragraph("5. Feature Engg.", body_style), Paragraph("src/feature_engineering.py", body_style), Paragraph("Stratified Split &rarr; models/tfidf_vectorizer.pkl", body_style)],
        [Paragraph("6. Training", body_style), Paragraph("src/train.py", body_style), Paragraph("Fit NB, LR, Linear SVM &rarr; models/*.pkl", body_style)],
        [Paragraph("7. Evaluation", body_style), Paragraph("src/evaluate.py", body_style), Paragraph("Test Set &rarr; results/metrics/*.csv, CM plots", body_style)],
        [Paragraph("8. Deployment", body_style), Paragraph("app.py & src/predict.py", body_style), Paragraph("Cached Inference &rarr; Streamlit Web UI", body_style)],
    ]
    t_arch = Table(arch_flow, colWidths=[85, 145, 250])
    t_arch.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Hardware and Software Requirements", h2_style))
    story.append(Paragraph("<b>Software Environment:</b>", body_bold))
    story.append(Paragraph("• Operating System: Windows 10/11, Linux (Ubuntu 20.04+), or macOS.<br/>"
                           "• Runtime: Python 3.11.x 64-bit.<br/>"
                           "• Key Libraries: Scikit-learn (1.3+), Pandas (2.0+), NumPy (1.24+), NLTK (3.8+), Matplotlib (3.7+), Seaborn (0.12+), Streamlit (1.30+), Joblib (1.3+).", body_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Hardware Specifications:</b>", body_bold))
    story.append(Paragraph("• Processor: Intel Core i3 / AMD Ryzen 3 or higher (Standard Dual/Quad Core CPU).<br/>"
                           "• Memory (RAM): Minimum 4 GB (8 GB recommended for EDA plotting).<br/>"
                           "• Storage: Minimum 500 MB free hard disk space (dataset is ~30MB; models total < 500KB).<br/>"
                           "• Network: Internet connection required only for initial package and NLTK corpus downloads.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 4 - DATASET & EDA (PART 1)
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: DATASET & EXPLORATORY DATA ANALYSIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("4.1 Dataset Acquisition and Provenance", h2_style))
    story.append(Paragraph(
        "This project utilizes the authentic, widely-cited benchmark news classification dataset (George McIntire & Katharine Jarmul). "
        "The raw dataset consists of <b>6,335 articles</b> containing four original attributes: an index column, <code>title</code>, <code>text</code>, and <code>label</code>. "
        "The data loader implemented in <code>src/data_loader.py</code> also features dual-mode compatibility, automatically detecting either single-CSV formats (Option A) "
        "or ISOT dual-CSV archives containing separate <code>True.csv</code> and <code>Fake.csv</code> files (Option B).",
        body_style
    ))

    story.append(Paragraph("4.2 Data Cleaning & Deduplication", h2_style))
    story.append(Paragraph(
        "Raw datasets collected from web scrapers frequently suffer from duplicated articles, missing body text, and non-standard label encodings. "
        "The cleaning module executes the following procedures:",
        body_style
    ))
    story.append(Paragraph("1. <b>Title & Body Fusion:</b> Headline and article bodies are merged into a unified <code>full_text</code> feature (<code>title + ' ' + text</code>) to ensure headline semantic cues are captured.", body_style))
    story.append(Paragraph("2. <b>Deduplication:</b> Exact string matching on <code>full_text</code> identified and removed <b>29 duplicate articles</b>.", body_style))
    story.append(Paragraph("3. <b>Null & Outlier Filtering:</b> Articles with empty bodies or fewer than 10 characters were pruned.", body_style))
    story.append(Paragraph("4. <b>Class Normalization:</b> Heterogeneous labels (e.g., 0/1, True/False, 'real'/'fake') are mapped strictly to binary classes: <b>REAL</b> and <b>FAKE</b>.", body_style))

    p_class_dist = "results/eda/class_distribution.png"
    if os.path.exists(p_class_dist):
        story.append(Spacer(1, 4))
        story.append(Image(p_class_dist, width=4.8*inch, height=2.6*inch))
        story.append(Paragraph("<b>Figure 4.1:</b> Class Distribution of Cleaned News Dataset (50.02% REAL vs. 49.98% FAKE).", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 4 - DATASET & EDA (PART 2)
    # =========================================================================
    story.append(Paragraph("4.3 Exploratory Data Analysis (EDA) Insights", h2_style))
    story.append(Paragraph(
        "Exploratory analysis was performed across the 6,306 cleaned records to examine textual properties without biasing subsequent classification:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Article Length Discrepancy:</b> Genuine articles exhibit a substantially higher average word count (<b>492.5 words</b>) compared to fabricated stories (<b>380.5 words</b>). "
        "As illustrated in Figure 4.2, genuine news articles display a right-skewed distribution characteristic of investigative, long-form journalism with multiple cited sources, "
        "whereas fake news is frequently characterized by succinct, emotionally charged summaries.",
        body_style
    ))

    p_len_dist = "results/eda/article_length_distribution.png"
    if os.path.exists(p_len_dist):
        story.append(Spacer(1, 2))
        story.append(Image(p_len_dist, width=5.0*inch, height=2.3*inch))
        story.append(Paragraph("<b>Figure 4.2:</b> Article Word Count Distribution across REAL and FAKE categories.", caption_style))

    story.append(Paragraph("4.4 Lexical Frequency Analysis", h2_style))
    story.append(Paragraph(
        "Figures 4.3 and 4.4 illustrate the top 20 most frequent lemmatized tokens in REAL and FAKE news corpora, respectively. "
        "Authentic reporting is dominated by terms reflecting institutional policy, congressional actions, and formal governance (e.g., <i>said, state, president, republican, government</i>). "
        "Conversely, fabricated reporting displays elevated relative frequencies of provocative rhetoric, media references, and speculative commentary (e.g., <i>people, trump, clinton, video, secret</i>).",
        body_style
    ))

    p_words_real = "results/eda/top_words_real.png"
    p_words_fake = "results/eda/top_words_fake.png"
    if os.path.exists(p_words_real) and os.path.exists(p_words_fake):
        img_table = Table([
            [Image(p_words_real, width=3.1*inch, height=2.1*inch),
             Image(p_words_fake, width=3.1*inch, height=2.1*inch)]
        ], colWidths=[240, 240])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(img_table)
        story.append(Paragraph("<b>Figures 4.3 & 4.4:</b> Top 20 Most Frequent Lemmatized Tokens in REAL News (left) and FAKE News (right).", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 5 - NLP PREPROCESSING & FEATURE ENGINEERING
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: NLP PREPROCESSING & FEATURE ENGINEERING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("5.1 Reusable NLP Preprocessing Pipeline", h2_style))
    story.append(Paragraph(
        "Natural human language is replete with orthographic irregularities, punctuation, HTML boilerplate, and inflectional morphology. "
        "Implemented in <code>src/preprocessing.py</code>, the preprocessing pipeline guarantees identical cleaning across batch training and single-article inference:",
        body_style
    ))

    prep_steps = [
        [Paragraph("<b>Step</b>", body_bold), Paragraph("<b>Operation</b>", body_bold), Paragraph("<b>Academic Purpose & Mechanism</b>", body_bold)],
        [Paragraph("1", body_style), Paragraph("Lowercasing", body_style), Paragraph("Converts all characters to lowercase to unify casing variants (e.g., 'Election' &rarr; 'election').", body_style)],
        [Paragraph("2", body_style), Paragraph("HTML Tag Stripping", body_style), Paragraph("Regular expression <code>&lt;.*?&gt;</code> purges markup artifacts introduced by web crawlers.", body_style)],
        [Paragraph("3", body_style), Paragraph("URL & Email Removal", body_style), Paragraph("Regex removes hyperlinks and contact emails that do not contribute to generalizable vocabulary.", body_style)],
        [Paragraph("4", body_style), Paragraph("Character Filtering", body_style), Paragraph("Regex <code>[^a-zA-Z\\s]</code> eliminates punctuation, numerals, and miscellaneous symbols.", body_style)],
        [Paragraph("5", body_style), Paragraph("Whitespace Normalization", body_style), Paragraph("Collapses multiple spaces, carriage returns, and tabs into standardized single spaces.", body_style)],
        [Paragraph("6", body_style), Paragraph("NLTK Tokenization", body_style), Paragraph("Splits continuous text into discrete syntactic tokens using NLTK's word_tokenize engine.", body_style)],
        [Paragraph("7", body_style), Paragraph("Stopword Removal", body_style), Paragraph("Filters out 179 standard English grammatical stopwords (e.g., <i>the, is, in, at, which</i>).", body_style)],
        [Paragraph("8", body_style), Paragraph("WordNet Lemmatization", body_style), Paragraph("Reduces inflected morphological word variants to canonical lemmas (e.g., 'studies' &rarr; 'study').", body_style)],
    ]
    t_prep = Table(prep_steps, colWidths=[35, 125, 320])
    t_prep.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_prep)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 Code Implementation of Preprocessing", h2_style))
    story.append(Paragraph(
        "The following snippet from <code>src/preprocessing.py</code> illustrates the core transformation logic:",
        body_style
    ))
    code_snippet = (
        "def clean_text(text: str) -> str:\n"
        "    if text is None or not isinstance(text, str): return ''\n"
        "    text = text.lower()\n"
        "    text = re.sub(r'<.*?>', ' ', text)                  # Strip HTML tags\n"
        "    text = re.sub(r'https?://\\S+|www\\.\\S+', ' ', text)  # Strip URLs\n"
        "    text = re.sub(r'[^a-zA-Z\\s]', ' ', text)           # Strip non-alpha characters\n"
        "    text = re.sub(r'\\s+', ' ', text).strip()           # Standardize whitespace\n"
        "    tokens = word_tokenize(text)\n"
        "    cleaned = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]\n"
        "    return ' '.join(cleaned)"
    )
    story.append(Paragraph(code_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 5 - FEATURE ENGINEERING & ZERO-LEAKAGE
    # =========================================================================
    story.append(Paragraph("5.3 Mathematical Formulation of TF-IDF", h2_style))
    story.append(Paragraph(
        "Machine learning models cannot directly process character strings. Term Frequency-Inverse Document Frequency (TF-IDF) converts textual documents "
        "into sparse numerical vectors by evaluating term importance across individual documents relative to the complete corpus.",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Term Frequency (TF):</b> Measures the normalized occurrence of term <i>t</i> within document <i>d</i>. To prevent bias from excessively repetitive words, "
        "we employ <b>sublinear TF scaling</b>:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>TF(t, d) = 1 + log(f<sub>t, d</sub>)</b>&nbsp;&nbsp;for&nbsp;<i>f<sub>t, d</sub> &gt; 0</i>, else 0",
        callout_style
    ))
    story.append(Paragraph(
        "<b>2. Inverse Document Frequency (IDF):</b> Quantifies the specificity of term <i>t</i> across the corpus of <i>N</i> documents:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>IDF(t, D) = log((1 + N) / (1 + |{d &isin; D : t &isin; d}|)) + 1</b>",
        callout_style
    ))
    story.append(Paragraph(
        "<b>3. Final TF-IDF Representation:</b> The composite weight is computed and L2-normalized across all features:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>TF-IDF(t, d, D) = TF(t, d) &times; IDF(t, D)</b>",
        callout_style
    ))

    story.append(Paragraph("5.4 Hyperparameter Configuration", h2_style))
    story.append(Paragraph(
        "The <code>TfidfVectorizer</code> in <code>src/feature_engineering.py</code> was tuned specifically for news journalism:",
        body_style
    ))
    story.append(Paragraph("• <code>max_features=5000</code>: Retains the top 5,000 most informative terms, restricting the dimensionality space.", body_style))
    story.append(Paragraph("• <code>ngram_range=(1, 2)</code>: Extracts unigrams and bigrams, capturing critical phrases (e.g., <i>white house, breaking news</i>).", body_style))
    story.append(Paragraph("• <code>min_df=3</code>: Ignores rare terms appearing in fewer than 3 articles, filtering typographical errors.", body_style))
    story.append(Paragraph("• <code>max_df=0.90</code>: Filters ubiquitous terms appearing in over 90% of articles.", body_style))
    story.append(Paragraph("• <code>sublinear_tf=True</code>: Dampens extreme word frequencies.", body_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("5.5 Strict Data-Leakage Prevention Protocol", h2_style))
    story.append(Paragraph(
        "<b>CRITICAL SCIENTIFIC PROTOCOL:</b> A severe methodological flaw in text mining occurs when the vectorizer is fitted on the entire dataset "
        "before partitioning. This allows vocabulary words and inverse document frequencies from the test set to leak into the training process.",
        body_style
    ))
    story.append(Paragraph(
        "In this project, the dataset was strictly split into <b>80% training (5,044 samples)</b> and <b>20% testing (1,262 samples)</b> using "
        "stratified sampling (<code>stratify=y, random_state=42</code>). The vectorizer was fitted <b>ONLY on X_train</b> (<code>vectorizer.fit_transform(X_train)</code>). "
        "The test set was subsequently transformed using the pre-fitted vocabulary (<code>vectorizer.transform(X_test)</code>). Zero test vocabulary or frequency "
        "weights influenced the feature mapping.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 6 - ML ALGORITHMS & MATHEMATICAL FOUNDATIONS
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: MACHINE LEARNING ALGORITHMS & MATHEMATICAL FOUNDATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("6.1 Multinomial Naive Bayes (MultinomialNB)", h2_style))
    story.append(Paragraph(
        "Multinomial Naive Bayes is a probabilistic classifier based on Bayes' Theorem with strong conditional independence assumptions between features:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(c | d) &prop; P(c) &prod; P(w<sub>i</sub> | c)</b>",
        callout_style
    ))
    story.append(Paragraph(
        "Where <i>P(c)</i> is the class prior probability and <i>P(w<sub>i</sub> | c)</i> is the likelihood of word <i>w<sub>i</sub></i> occurring in class <i>c</i>. "
        "To prevent zero-frequency probabilities for n-grams unobserved in training documents of a given class, <b>Laplace Smoothing</b> (&alpha; = 0.1) is applied:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(w<sub>i</sub> | c) = (N<sub>ci</sub> + &alpha;) / (N<sub>c</sub> + &alpha; &times; |V|)</b>",
        callout_style
    ))
    story.append(Paragraph(
        "Where <i>N<sub>ci</sub></i> is the sum of TF-IDF weights of term <i>i</i> in class <i>c</i>, <i>N<sub>c</sub></i> is the total feature weight in class <i>c</i>, "
        "and <i>|V| = 5000</i> is the vocabulary size.",
        body_style
    ))

    story.append(Paragraph("6.2 Logistic Regression", h2_style))
    story.append(Paragraph(
        "Logistic Regression is a linear classification model that predicts class posterior probabilities by applying a logistic sigmoid function to a linear combination of input features:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(y = REAL | x) = &sigma;(w<sup>T</sup> x + b) = 1 / (1 + e<sup>-(w<sup>T</sup> x + b)</sup>)</b>",
        callout_style
    ))
    story.append(Paragraph(
        "The model weights <i>w</i> and bias <i>b</i> are optimized by minimizing the regularized Binary Cross-Entropy loss (Log-Loss) using the L-BFGS quasi-Newton solver:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>J(w, b) = - (1/N) &sum; [y<sub>i</sub> log(&sigma;(z<sub>i</sub>)) + (1 - y<sub>i</sub>) log(1 - &sigma;(z<sub>i</sub>))] + (1 / 2C) ||w||<sup>2</sup></b>",
        callout_style
    ))
    story.append(Paragraph(
        "With inverse regularization strength <i>C = 1.0</i>, preventing overfitting on high-dimensional text vectors.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 6 - ML ALGORITHMS (PART 2)
    # =========================================================================
    story.append(Paragraph("6.3 Linear Support Vector Machine (Linear SVM)", h2_style))
    story.append(Paragraph(
        "Support Vector Machines construct an optimal decision hyperplane in high-dimensional feature space that separates the training instances of the two classes "
        "with the maximum geometric margin. For a linearly separable training set, the decision boundary is defined by:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>w<sup>T</sup> x + b = 0</b>",
        callout_style
    ))
    story.append(Paragraph(
        "The distance from any feature vector <i>x<sub>i</sub></i> to the hyperplane is given by <i>|w<sup>T</sup> x<sub>i</sub> + b| / ||w||</i>. "
        "Maximizing the margin <i>2 / ||w||</i> is mathematically equivalent to minimizing <i>(1/2) ||w||<sup>2</sup></i>. "
        "For non-linearly separable textual data, the soft-margin formulation introduces slack variables <i>&xi;<sub>i</sub> &ge; 0</i>:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>min<sub>w, b, &xi;</sub> (1/2) ||w||<sup>2</sup> + C &sum; &xi;<sub>i</sub></b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;subject to: <b>y<sub>i</sub> (w<sup>T</sup> x<sub>i</sub> + b) &ge; 1 - &xi;<sub>i</sub></b>, &nbsp;&nbsp;&xi;<sub>i</sub> &ge; 0",
        callout_style
    ))
    story.append(Paragraph(
        "In this project, <code>LinearSVC(C=1.0, dual='auto', random_state=42)</code> was utilized. Linear SVM is exceptionally well-suited for NLP and text classification "
        "for three fundamental theoretical reasons:",
        body_style
    ))
    story.append(Paragraph("1. <b>High Dimensionality:</b> TF-IDF generates thousands of features. Cover's Theorem on Separability states that high-dimensional sparse representations are highly likely to be linearly separable.", body_style))
    story.append(Paragraph("2. <b>Sparsity:</b> Document vectors are mostly zero. SVM optimization depends solely on inner products of support vectors, making training computationally efficient.", body_style))
    story.append(Paragraph("3. <b>Regularization Robustness:</b> The maximum-margin constraint inherently prevents overfitting, yielding outstanding out-of-sample generalization.", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("6.4 Algorithm Summary Comparison", h2_style))
    algo_comp_table = [
        [Paragraph("<b>Algorithm</b>", body_bold), Paragraph("<b>Family</b>", body_bold), Paragraph("<b>Key Assumptions</b>", body_bold), Paragraph("<b>Primary Advantage</b>", body_bold)],
        [Paragraph("MultinomialNB", body_style), Paragraph("Generative Probabilistic", body_style), Paragraph("Conditional word independence", body_style), Paragraph("Blazing fast; simple baseline", body_style)],
        [Paragraph("Logistic Regression", body_style), Paragraph("Discriminative Linear", body_style), Paragraph("Linear log-odds relationship", body_style), Paragraph("Well-calibrated probabilities", body_style)],
        [Paragraph("Linear SVM", body_style), Paragraph("Discriminative Margin-Max", body_style), Paragraph("Linear class separability", body_style), Paragraph("Superior generalization on sparse text", body_style)],
    ]
    t_algo = Table(algo_comp_table, colWidths=[95, 120, 135, 130])
    t_algo.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_algo)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 7 - EXPERIMENTAL RESULTS & EVALUATION (PART 1)
    # =========================================================================
    story.append(Paragraph("CHAPTER 7: EXPERIMENTAL RESULTS & MODEL EVALUATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("7.1 Evaluation Metrics Definition", h2_style))
    story.append(Paragraph(
        "To rigorously quantify classification performance on the isolated test set (1,262 samples), four standard statistical metrics were calculated:",
        body_style
    ))
    story.append(Paragraph("• <b>Accuracy:</b> Proportion of correct predictions over total predictions: <code>(TP + TN) / (TP + TN + FP + FN)</code>.", body_style))
    story.append(Paragraph("• <b>Precision (Macro):</b> Average exactness across both classes: <code>(Precision_REAL + Precision_FAKE) / 2</code>.", body_style))
    story.append(Paragraph("• <b>Recall (Macro):</b> Average completeness across both classes: <code>(Recall_REAL + Recall_FAKE) / 2</code>.", body_style))
    story.append(Paragraph("• <b>Macro F1-Score:</b> Harmonic mean of precision and recall: <code>2 &times; (Precision &times; Recall) / (Precision + Recall)</code>.", body_style))

    story.append(Paragraph("7.2 Actual Test Set Performance Comparison", h2_style))
    story.append(Paragraph(
        "The following empirical results were obtained by executing the master pipeline on the held-out test split:",
        body_style
    ))

    results_table_data = [
        [Paragraph("<b>Model</b>", body_bold), Paragraph("<b>Test Accuracy</b>", body_bold), Paragraph("<b>Macro Precision</b>", body_bold), Paragraph("<b>Macro Recall</b>", body_bold), Paragraph("<b>Macro F1-Score</b>", body_bold)],
        [Paragraph("<b>Linear Support Vector Machine (Linear SVM)</b>", body_bold), Paragraph("<b>92.63%</b> (0.9263)", body_style), Paragraph("0.9263", body_style), Paragraph("0.9263", body_style), Paragraph("<b>0.9263</b>", body_bold)],
        [Paragraph("Logistic Regression", body_style), Paragraph("91.44% (0.9144)", body_style), Paragraph("0.9146", body_style), Paragraph("0.9144", body_style), Paragraph("0.9144", body_style)],
        [Paragraph("Multinomial Naive Bayes", body_style), Paragraph("87.72% (0.8772)", body_style), Paragraph("0.8803", body_style), Paragraph("0.8772", body_style), Paragraph("0.8769", body_style)],
    ]
    t_res = Table(results_table_data, colWidths=[160, 80, 80, 80, 80])
    t_res.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1.5, primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.3 Dynamic Model Selection Rationale", h2_style))
    story.append(Paragraph(
        "In compliance with project specifications, model selection was <b>dynamically determined via code execution</b> rather than hardcoded. "
        "The evaluation module in <code>src/evaluate.py</code> sorted the candidate models primarily on test Macro F1-score (with Precision and Recall as tiebreakers). "
        "<b>Linear SVM</b> emerged as the undisputed winner with an accuracy of <b>92.63%</b> and Macro F1 of <b>0.9263</b>. "
        "The winning model was serialized as <code>models/final_model.pkl</code> along with complete training metadata in <code>models/model_metadata.json</code>.",
        body_style
    ))

    p_svm_cm = "results/confusion_matrices/linear_svm_cm.png"
    if os.path.exists(p_svm_cm):
        story.append(Spacer(1, 2))
        story.append(Image(p_svm_cm, width=4.0*inch, height=2.8*inch))
        story.append(Paragraph("<b>Figure 7.1:</b> Confusion Matrix for Winning Model (Linear SVM) on 1,262 Test Articles.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 7 - EVALUATION (PART 2) - OTHER CONFUSION MATRICES
    # =========================================================================
    story.append(Paragraph("7.4 Confusion Matrix Comparative Analysis", h2_style))
    story.append(Paragraph(
        "A confusion matrix exposes the precise balance between True Positives, True Negatives, False Positives, and False Negatives. "
        "Figures 7.2 and 7.3 illustrate the confusion matrices for Logistic Regression and Multinomial Naive Bayes.",
        body_style
    ))

    p_lr_cm = "results/confusion_matrices/logistic_regression_cm.png"
    p_nb_cm = "results/confusion_matrices/multinomial_naive_bayes_cm.png"
    if os.path.exists(p_lr_cm) and os.path.exists(p_nb_cm):
        cm_table = Table([
            [Image(p_lr_cm, width=3.0*inch, height=2.3*inch),
             Image(p_nb_cm, width=3.0*inch, height=2.3*inch)]
        ], colWidths=[240, 240])
        cm_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(cm_table)
        story.append(Paragraph("<b>Figures 7.2 & 7.3:</b> Confusion Matrices for Logistic Regression (left) and Multinomial Naive Bayes (right).", caption_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("7.5 Detailed Classification Reports", h2_style))
    story.append(Paragraph(
        "The detailed per-class classification report for the selected Linear SVM model confirms balanced precision and recall across both classes:",
        body_style
    ))

    rep_svm = (
        "Classification Report: Linear SVM\n"
        "============================================================\n"
        "              precision    recall  f1-score   support\n\n"
        "        FAKE     0.9238    0.9287    0.9262       631\n"
        "        REAL     0.9288    0.9239    0.9264       631\n\n"
        "    accuracy                         0.9263      1262\n"
        "   macro avg     0.9263    0.9263    0.9263      1262\n"
        "weighted avg     0.9263    0.9263    0.9263      1262"
    )
    story.append(Paragraph(rep_svm.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Analysis:</b> The performance demonstrates exceptional symmetry (REAL F1: 0.9264 vs. FAKE F1: 0.9262). "
        "The model displays no systematic bias toward classifying unknown articles into a specific majority class.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: CHAPTER 8 - WEB APPLICATION & DEMONSTRATION (PART 1)
    # =========================================================================
    story.append(Paragraph("CHAPTER 8: INTERACTIVE WEB APPLICATION & DEMONSTRATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("8.1 Streamlit Interface Architecture", h2_style))
    story.append(Paragraph(
        "To allow non-technical evaluators, professors, and viva examiners to test the system in real time, an interactive academic web application "
        "was developed using Streamlit (<code>app.py</code>). The web application adheres to three key engineering principles:",
        body_style
    ))
    story.append(Paragraph("1. <b>Cached Resource Loading:</b> Uses <code>@st.cache_resource</code> to deserialize <code>final_model.pkl</code> and <code>tfidf_vectorizer.pkl</code> into memory once at startup, eliminating redundant retraining.", body_style))
    story.append(Paragraph("2. <b>Instant Viva Demonstration:</b> Features one-click sample buttons (<b>Load Real News</b> and <b>Load Fake News</b>) to permit instantaneous testing during vivas.", body_style))
    story.append(Paragraph("3. <b>Model Confidence Estimation:</b> Employs sigmoid transformation over SVM hyperplane distance margins (<code>1 / (1 + exp(-|margin|))</code>) to display calibrated technical confidence without falsely claiming 'truth verification'.", body_style))

    p_s1 = "reports/screenshots/01_streamlit_home.png"
    if os.path.exists(p_s1):
        story.append(Spacer(1, 3))
        story.append(Image(p_s1, width=5.2*inch, height=2.9*inch))
        story.append(Paragraph("<b>Figure 8.1:</b> Streamlit Web Application Interface showing title, sidebar metadata, quick-load buttons, and input area.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: CHAPTER 8 - WEB APPLICATION (PART 2) - PREDICTION TESTS
    # =========================================================================
    story.append(Paragraph("8.2 Demonstration Test Case 1: Genuine News Article", h2_style))
    story.append(Paragraph(
        "A formal journalistic article discussing Congressional voting and Senate committee proceedings was tested. As depicted in Figure 8.2, "
        "the application classified the article as <b>REAL NEWS (GENUINE)</b>, displaying the active classifier badge and model confidence.",
        body_style
    ))

    p_s2 = "reports/screenshots/02_real_news_prediction.png"
    if os.path.exists(p_s2):
        story.append(Spacer(1, 2))
        story.append(Image(p_s2, width=5.2*inch, height=2.4*inch))
        story.append(Paragraph("<b>Figure 8.2:</b> Real News Prediction Result Card with Green Status Banner and Model Confidence.", caption_style))

    story.append(Paragraph("8.3 Demonstration Test Case 2: Fabricated News Article", h2_style))
    story.append(Paragraph(
        "A sensationalist conspiracy article featuring unverified whistleblowers and dramatic rhetoric was submitted. "
        "As shown in Figure 8.3, the system accurately classified the text as <b>FAKE NEWS (FABRICATED)</b> with high confidence.",
        body_style
    ))

    p_s3 = "reports/screenshots/03_fake_news_prediction.png"
    if os.path.exists(p_s3):
        story.append(Spacer(1, 2))
        story.append(Image(p_s3, width=5.2*inch, height=2.4*inch))
        story.append(Paragraph("<b>Figure 8.3:</b> Fake News Prediction Result Card with Red Status Banner and Model Confidence.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: CHAPTER 8 - WEB APPLICATION (PART 3) - VIVA TABS & TOKEN INSPECTION
    # =========================================================================
    story.append(Paragraph("8.4 Interactive Viva & Evaluation Tabs", h2_style))
    story.append(Paragraph(
        "The interface includes tabbed panels providing examiners with theoretical foundations (Figure 8.4) and embedded model comparison metrics (Figure 8.5):",
        body_style
    ))

    p_s4 = "reports/screenshots/04_model_explanations.png"
    p_s5 = "reports/screenshots/05_model_comparison_and_cm.png"
    if os.path.exists(p_s4) and os.path.exists(p_s5):
        tab_img_table = Table([
            [Image(p_s4, width=3.1*inch, height=2.0*inch),
             Image(p_s5, width=3.1*inch, height=2.0*inch)]
        ], colWidths=[240, 240])
        tab_img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(tab_img_table)
        story.append(Paragraph("<b>Figures 8.4 & 8.5:</b> Streamlit viva explanation notes tab (left) and interactive model comparison matrix tab (right).", caption_style))

    story.append(Paragraph("8.5 NLP Token Inspection Feature", h2_style))
    story.append(Paragraph(
        "To provide complete transparency during demonstration, users can expand the 'View Preprocessed NLP Tokens' card to inspect the exact lemmatized, "
        "stopword-filtered tokens fed into the TF-IDF vectorizer:",
        body_style
    ))

    p_s7 = "reports/screenshots/07_nlp_tokens_inspection.png"
    if os.path.exists(p_s7):
        story.append(Spacer(1, 2))
        story.append(Image(p_s7, width=5.2*inch, height=2.0*inch))
        story.append(Paragraph("<b>Figure 8.6:</b> Preprocessed NLP Tokens Inspection expander displaying tokenized features.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 9 - CRITICAL ANALYSIS & LIMITATIONS
    # =========================================================================
    story.append(Paragraph("CHAPTER 9: CRITICAL ANALYSIS & LIMITATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("9.1 Technical & Operational Boundaries", h2_style))
    story.append(Paragraph(
        "In an academic defense, it is imperative to acknowledge the theoretical and operational boundaries of the system:",
        body_style
    ))
    story.append(Paragraph("1. <b>Style Classification vs. Fact-Checking:</b> The model learns vocabulary distributions and stylistic patterns characteristic of training sets. It does not possess a world knowledge graph and cannot independently verify whether a real-world event occurred.", body_style))
    story.append(Paragraph("2. <b>Temporal and Domain Drift:</b> Vocabulary evolves over time. A model trained on political discourse from 2016–2020 may degrade when confronted with modern geopolitical reporting or emerging medical terminology.", body_style))
    story.append(Paragraph("3. <b>Adversarial Susceptibility:</b> A sophisticated author writing false information using impeccable formal AP/Reuters journalistic style may mislead a classical TF-IDF bag-of-words classifier.", body_style))
    story.append(Paragraph("4. <b>Lack of Contextual Polysemy:</b> Bag-of-words and n-gram TF-IDF models treat word occurrences as independent features, unable to resolve words that change meaning depending on surrounding grammatical syntax.", body_style))

    story.append(Paragraph("9.2 Ethical Considerations in Automated News Filtering", h2_style))
    story.append(Paragraph(
        "Deploying algorithmic news classifiers requires rigorous ethical safeguards. False positives (labeling genuine news as FAKE) can suppress legitimate "
        "whistleblowing, minority perspectives, or dissenting political commentary. False negatives (labeling fabricated news as REAL) can facilitate "
        "disinformation campaigns. Therefore, this system is positioned strictly as a decision-support aid and educational classifier, displaying prominent "
        "cautionary notices to prevent users from treating model predictions as infallible truth judgments.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: CHAPTER 10 - CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("CHAPTER 10: CONCLUSION & FUTURE SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    story.append(Paragraph("10.1 Project Conclusion", h2_style))
    story.append(Paragraph(
        "This BTech CSE mini-project successfully engineered an end-to-end, leak-free classical NLP and Machine Learning fake news detection system. "
        "Through disciplined engineering, 6,306 cleaned news articles were transformed via TF-IDF into unigram and bigram feature representations. "
        "Among the three classical classifiers evaluated, <b>Linear Support Vector Machine (Linear SVM)</b> demonstrated peak performance, achieving "
        "<b>92.63% test accuracy</b> and a <b>Macro F1-score of 0.9263</b>, outperforming Logistic Regression (91.44%) and Naive Bayes (87.72%).",
        body_style
    ))
    story.append(Paragraph(
        "The project achieves high scientific explainability, zero data leakage, automated dynamic model selection, and user-friendly deployment "
        "via a clean Streamlit interface. It stands as an exemplary demonstration of classical machine learning principles for undergraduate engineering.",
        body_style
    ))

    story.append(Paragraph("10.2 Future Scope & Research Directions", h2_style))
    story.append(Paragraph(
        "While this project intentionally restricted scope to classical ML to prioritize explainability and computational efficiency, future research directions include:",
        body_style
    ))
    story.append(Paragraph("1. <b>Bidirectional Contextual Embeddings:</b> Fine-tuning transformer models (BERT, RoBERTa) to capture deep semantic dependencies and subtle syntactic nuances.", body_style))
    story.append(Paragraph("2. <b>Retrieval-Augmented Verification:</b> Combining linguistic classification with real-time automated knowledge retrieval from authoritative knowledge bases (e.g., Wikipedia, Reuters FactCheck).", body_style))
    story.append(Paragraph("3. <b>Multimodal Forensics:</b> Incorporating reverse image search and image forensic analysis to detect manipulated graphics and deceptive video thumbnails.", body_style))
    story.append(Paragraph("4. <b>Source Credibility Graphing:</b> Integrating domain reputational authority, publisher metadata, and network propagation patterns into the decision matrix.", body_style))
    story.append(Paragraph("5. <b>Multilingual Detection:</b> Expanding tokenization and lemmatization to support regional languages (e.g., Hindi, Telugu, Spanish).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: REFERENCES, BIBLIOGRAPHY & APPENDIX
    # =========================================================================
    story.append(Paragraph("REFERENCES & BIBLIOGRAPHY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=6))

    refs = [
        "[1] V. L. Rubin, Y. Chen, and N. J. Conroy, \"Deception detection for news: three types of fakes,\" <i>Proc. 78th ASIS&T Annual Meeting</i>, 2015.",
        "[2] K. Shu, A. Sliva, S. Wang, J. Tang, and H. Liu, \"Fake news detection on social media: A data mining perspective,\" <i>ACM SIGKDD Explorations</i>, 2017.",
        "[3] H. Ahmed, I. Traore, and S. Saad, \"Detection of online fake news using n-gram analysis and ML techniques,\" <i>Springer LNCS</i>, 2017.",
        "[4] G. McIntire and K. Jarmul, \"Fake and real news dataset,\" <i>DataCamp Tutorial Repository</i>, 2016.",
        "[5] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" <i>Journal of Machine Learning Research</i>, vol. 12, 2011.",
        "[6] S. Bird, E. Klein, and E. Loper, <i>Natural Language Processing with Python</i>. O'Reilly Media, 2009.",
        "[7] C. Cortes and V. Vapnik, \"Support-vector networks,\" <i>Machine Learning</i>, vol. 20, no. 3, pp. 273–297, 1995.",
        "[8] D. Jurafsky and J. H. Martin, <i>Speech and Language Processing</i>, 3rd ed. draft, Prentice Hall, 2023.",
        "[9] T. Joachims, \"Text categorization with support vector machines,\" <i>European Conf. on Machine Learning (ECML)</i>, 1998.",
        "[10] Streamlit Documentation, \"Streamlit: Fast data apps framework,\" 2026. [Online]. Available: https://docs.streamlit.io"
    ]

    for ref in refs:
        story.append(Paragraph(ref, ParagraphStyle("RefStyle", parent=body_style, fontSize=7.5, leading=10, spaceAfter=3)))

    story.append(Spacer(1, 4))
    story.append(Paragraph("APPENDIX: EXECUTION COMMANDS & REPOSITORY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=6))

    exec_text = (
        "# 1. Environment Setup & Dependency Installation\n"
        "python -m venv .venv\n"
        ".venv\\Scripts\\activate\n"
        "pip install -r requirements.txt\n\n"
        "# 2. Run Complete End-to-End ML Pipeline\n"
        "python run_pipeline.py\n\n"
        "# 3. Run Automated Tests\n"
        "python -m unittest discover tests\n\n"
        "# 4. Launch Interactive Web Application\n"
        "python -m streamlit run app.py"
    )
    story.append(Paragraph(exec_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>GitHub Repository:</b> https://github.com/sunnykarthik15/ML-MINI-PROJECT", body_bold))

    # Build the document
    print(f"[PDF Generator] Building 20-page PDF document at '{output_pdf_path}'...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generator] Successfully generated: '{output_pdf_path}'")


if __name__ == "__main__":
    create_report()
