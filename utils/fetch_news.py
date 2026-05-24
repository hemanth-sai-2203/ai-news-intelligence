import os
import requests
import urllib.parse
from dotenv import load_dotenv
import feedparser
import re
from datetime import datetime
import google.generativeai as genai

load_dotenv()

def clean_search_query(topic):
    """
    Stage 1: Scrub the query of common stop words that break exact-match APIs.
    """
    topic = topic.lower()
    junk_words = ['latest', 'news', 'today', 'yesterday', 'breaking', 'update', 'about', 'give me', 'show me', 'the']
    for word in junk_words:
        topic = re.sub(rf'\b{word}\b', '', topic)
    # Remove extra spaces
    topic = re.sub(r'\s+', ' ', topic).strip()
    return topic

def llm_query_pivot(topic):
    """
    Stage 3: Ask Gemini to optimize the search keyword.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        return topic
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"The user searched for '{topic}' on a news API, but 0 articles were found. Please extract the core entity or generate a single, highly searchable keyword phrase (1-3 words max) that will return good news results. Only return the search term, nothing else."
        
        response = model.generate_content(prompt)
        new_topic = response.text.strip().replace('"', '').replace("'", "")
        return new_topic if new_topic else topic
    except:
        return topic

def _fetch_gnews(topic, max_articles):
    load_dotenv(override=True)
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return [], "GNews API Key missing"
        
    encoded_topic = urllib.parse.quote(topic)
    url = f"https://gnews.io/api/v4/search?q={encoded_topic}&lang=en&max={max_articles}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", []), None
    except:
        pass
    return [], "GNews failed"

def _fetch_google_rss(topic, max_articles):
    encoded_topic = urllib.parse.quote(topic)
    url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:max_articles]:
            articles.append({
                'title': entry.title,
                # Google RSS descriptions contain HTML, we just fallback to title if messy
                'description': entry.title, 
                'source': {'name': entry.source.title if hasattr(entry, 'source') else 'Google News'},
                'url': entry.link,
                'publishedAt': entry.published if hasattr(entry, 'published') else datetime.now().isoformat(),
                'image': ''
            })
        return articles, None
    except:
        return [], "RSS failed"

def _fetch_duckduckgo(topic, max_articles):
    articles = []
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = ddgs.news(topic, max_results=max_articles)
            if results:
                for r in list(results):
                    articles.append({
                        'title': r.get('title', ''),
                        'description': r.get('body', ''),
                        'source': {'name': r.get('source', 'DuckDuckGo')},
                        'url': r.get('url', ''),
                        'publishedAt': r.get('date', datetime.now().isoformat()),
                        'image': r.get('image', '')
                    })
    except:
        pass
    return articles, None

def fetch_live_news(raw_topic, max_articles=10):
    """
    The Cascade Aggregator.
    Returns (articles, error_message, metadata_dict)
    """
    topic = clean_search_query(raw_topic)
    if not topic:
        topic = raw_topic
        
    metadata = {'original': raw_topic, 'searched': topic, 'source': None, 'pivoted': False}

    # 1. Try GNews
    articles, _ = _fetch_gnews(topic, max_articles)
    if articles:
        metadata['source'] = 'GNews API'
        return articles, None, metadata
        
    # 2. Try Google RSS
    articles, _ = _fetch_google_rss(topic, max_articles)
    if articles:
        metadata['source'] = 'Google News RSS (Fallback)'
        return articles, None, metadata
        
    # 3. Try DuckDuckGo
    articles, _ = _fetch_duckduckgo(topic, max_articles)
    if articles:
        metadata['source'] = 'DuckDuckGo News (Fallback)'
        return articles, None, metadata
        
    # 4. LLM Pivot
    pivoted_topic = llm_query_pivot(topic)
    if pivoted_topic.lower() != topic.lower():
        metadata['searched'] = pivoted_topic
        metadata['pivoted'] = True
        
        articles, _ = _fetch_google_rss(pivoted_topic, max_articles)
        if articles:
            metadata['source'] = 'Google News RSS (AI Pivoted)'
            return articles, None, metadata
            
        articles, _ = _fetch_duckduckgo(pivoted_topic, max_articles)
        if articles:
            metadata['source'] = 'DuckDuckGo News (AI Pivoted)'
            return articles, None, metadata

    return [], "All news sources returned 0 articles. The topic may be too obscure.", metadata
