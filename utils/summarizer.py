import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def generate_executive_summary(text):
    """
    Uses Google Gemini API to generate a high-quality executive summary.
    Falls back to extractive summarization if the API is unavailable.
    """
    if not text or len(text.split()) < 30:
        return "Not enough data to generate a meaningful summary."

    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")

    # If no API key, use fallback
    if not api_key or api_key == "your_google_api_key_here":
        return _extractive_fallback(text)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Truncate if too long
        words = text.split()
        if len(words) > 800:
            words = words[:800]
        truncated_text = " ".join(words)

        prompt = f"""You are an expert news intelligence analyst. Analyze the following collection of news article excerpts and write a professional executive summary.

Your summary should:
- Be exactly 1 paragraph (4-6 sentences)
- Highlight the key themes and major developments
- Mention the overall sentiment (positive, negative, or mixed)
- Note any risks, opportunities, or trends
- Be written in a professional, analytical tone

News Articles:
{truncated_text}

Executive Summary:"""

        response = model.generate_content(prompt)
        summary = response.text.strip()

        return summary if summary else _extractive_fallback(text)

    except Exception as e:
        return _extractive_fallback(text)


def _extractive_fallback(text):
    """
    NLTK-based extractive summarization as a reliable fallback.
    """
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    import heapq

    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)
        nltk.download('punkt', quiet=True)

    try:
        sentence_list = sent_tokenize(text)
        stopwords_set = set(stopwords.words('english'))

        word_frequencies = {}
        for word in word_tokenize(text):
            word = word.lower()
            if word not in stopwords_set and word.isalnum():
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        if not word_frequencies:
            return "Not enough meaningful content to summarize."

        max_freq = max(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        sentence_scores = {}
        for sent in sentence_list:
            if len(sent.split()) > 35:
                continue
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

        summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        return ' '.join(summary_sentences) or "Could not extract a meaningful summary."

    except Exception:
        return "Summary generation is currently unavailable."
