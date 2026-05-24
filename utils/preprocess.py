import re
import nltk
from nltk.corpus import stopwords
import os

def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

download_nltk_data()

def clean_text(text):
    """
    Cleans text data by removing URLs, symbols, and stopwords.
    """
    if not text:
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove symbols and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    
    stop_words = set(stopwords.words('english'))
    # Remove stopwords
    words = text.split()
    words = [w for w in words if w not in stop_words]
    
    return " ".join(words)
