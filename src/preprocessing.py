"""
NLP Preprocessing Module for Fake News Detection.

Provides reproducible text preprocessing including:
- Lowercasing
- HTML tag stripping
- URL removal
- Special character & punctuation removal
- Tokenization
- Stopword removal
- Lemmatization
- Reconstructing normalized clean text

Programmatically downloads necessary NLTK resources if not already present.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Track if NLTK resources have been initialized
_NLTK_INITIALIZED = False
_STOPWORDS_SET = None
_LEMMATIZER = None


def setup_nltk_resources() -> None:
    """Download required NLTK data programmatically if missing."""
    global _NLTK_INITIALIZED, _STOPWORDS_SET, _LEMMATIZER
    if _NLTK_INITIALIZED:
        return

    required_corpora = [
        ("corpora/stopwords", "stopwords"),
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]

    for corpus_path, corpus_name in required_corpora:
        try:
            nltk.data.find(corpus_path)
        except (LookupError, IndexError):
            try:
                nltk.download(corpus_name, quiet=True)
            except Exception as e:
                # If punkt_tab or omw fails on certain versions, log and continue
                print(f"[NLTK Setup Note] {corpus_name}: {e}")

    try:
        _STOPWORDS_SET = set(stopwords.words("english"))
    except Exception:
        nltk.download("stopwords", quiet=True)
        _STOPWORDS_SET = set(stopwords.words("english"))

    _LEMMATIZER = WordNetLemmatizer()
    _NLTK_INITIALIZED = True


def clean_text(text: str) -> str:
    """
    Apply full NLP cleaning pipeline to raw news text.

    Args:
        text (str): Raw news article text or title.

    Returns:
        str: Cleaned, tokenized, stopword-removed, and lemmatized text.
    """
    setup_nltk_resources()

    # 1. Handle missing, null, or non-string inputs
    if text is None or not isinstance(text, str):
        return ""

    # 2. Lowercase text
    text = text.lower()

    # 3. Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # 4. Remove URLs and hyperlinks
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # 5. Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # 6. Remove non-alphabetic characters (numbers, punctuation, symbols)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # 7. Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    # 8. Tokenize text (with regex fallback if punkt has tokenizer issue)
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()

    # 9. Remove stop words & single-character tokens, then lemmatize
    cleaned_tokens = []
    for token in tokens:
        if token not in _STOPWORDS_SET and len(token) > 1:
            try:
                lemmatized = _LEMMATIZER.lemmatize(token)
            except Exception:
                lemmatized = token
            cleaned_tokens.append(lemmatized)

    # 10. Reconstruct cleaned text
    return " ".join(cleaned_tokens)
