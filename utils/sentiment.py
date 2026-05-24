import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def download_vader():
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)

download_vader()
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Returns the sentiment of a given text.
    Classes: Positive, Neutral, Negative
    """
    if not text:
        return "Neutral", 0.0
    
    score = sia.polarity_scores(text)
    compound = score['compound']
    
    if compound >= 0.05:
        return "Positive", compound
    elif compound <= -0.05:
        return "Negative", compound
    else:
        return "Neutral", compound
