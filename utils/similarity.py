from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple, Dict
import spacy

# my favorite transformer model, don't judge me
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load('en_core_web_sm')

def get_embedding(text: str) -> np.ndarray:
    # magic happens here
    return model.encode(text)

def calculate_similarity(text1: str, text2: str) -> float:
    # let's see if these texts are soulmates
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    
    # math magic to find love
    similarity = np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )
    return float(similarity)

def extract_keywords(text: str, n_keywords: int = 10) -> List[str]:
    # time to find the important stuff
    doc = nlp(text)
    
    # collecting the good words
    keywords = []
    for token in doc:
        if (token.pos_ in ['NOUN', 'PROPN'] and 
            not token.is_stop and 
            len(token.text) > 2):
            keywords.append(token.text.lower())
    
    # counting words like a word accountant
    keyword_freq = {}
    for keyword in keywords:
        keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
    
    # sorting the winners
    sorted_keywords = sorted(keyword_freq.items(), 
                           key=lambda x: x[1], 
                           reverse=True)
    return [k[0] for k in sorted_keywords[:n_keywords]]

def compare_keywords(resume_keywords: List[str], 
                    job_keywords: List[str]) -> Dict[str, List[str]]:
    # let's play spot the difference
    resume_keywords_set = set(resume_keywords)
    job_keywords_set = set(job_keywords)
    
    # finding matches and misses
    matched = list(resume_keywords_set.intersection(job_keywords_set))
    missing = list(job_keywords_set - resume_keywords_set)
    
    return {
        'matched': matched,
        'missing': missing
    } 