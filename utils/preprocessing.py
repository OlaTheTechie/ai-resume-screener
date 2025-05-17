import spacy

# Load spacy model once for efficiency
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Preprocess text by:
    - Lowercasing
    - Removing extra whitespace
    - Lemmatizing tokens
    - Removing stopwords and punctuation
    """
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens).strip()
