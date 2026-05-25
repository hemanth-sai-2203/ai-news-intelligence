# AI News Intelligence & Sentiment Analytics Dashboard

> A real-time, AI-powered news intelligence platform that fetches live articles, classifies sentiment, calculates risk scores, and generates executive summaries — all in seconds.

**🚀 Live Application:** [View the Dashboard on Render](https://ai-news-intelligence-5old.onrender.com)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Classification](#project-classification)
3. [Architecture & Pipeline](#architecture--pipeline)
4. [File Structure](#file-structure)
5. [Tech Stack](#tech-stack)
6. [Core Modules (utils/)](#core-modules-utils)
7. [Key Features](#key-features)
8. [How It Works — Step by Step](#how-it-works--step-by-step)
9. [Setup & Local Run](#setup--local-run)
10. [Environment Variables](#environment-variables)
11. [Deployment](#deployment)
12. [Real-World Use Cases](#real-world-use-cases)

---

## Project Overview

The **AI News Intelligence Dashboard** is a full-stack, applied AI and data science project. It solves a critical problem: **information overload**. Given any topic (a company, a market, an event, or a person), the system automatically:

1. Fetches live news articles from multiple sources using a multi-tiered cascade engine
2. Cleans and preprocesses the raw text using NLP techniques
3. Classifies the sentiment of each article (Positive / Neutral / Negative)
4. Calculates a composite Risk Score based on negative signals and alarming language
5. Generates a professional AI executive summary using Google Gemini LLM
6. Visualizes everything through an interactive web dashboard

---

## Project Classification

This project sits at the intersection of **Applied AI** and **Data Science (DS)**:

| Domain | Component |
|---|---|
| **Data Engineering** | Multi-source live data ingestion pipeline (GNews, Google RSS, DuckDuckGo) |
| **NLP / Data Science** | Text cleaning, tokenization, VADER sentiment classification |
| **Applied AI / LLM** | Google Gemini for executive summary generation and autonomous query pivoting |
| **Data Analytics** | Risk score engineering, keyword frequency analysis |
| **Data Visualization** | Interactive Plotly charts, Word Cloud, Sentiment Timeline |
| **Web App** | Streamlit-powered full-stack dashboard deployed on Render |

---

## Architecture & Pipeline

```
User Input (Topic)
        │
        ▼
┌───────────────────────────────────────────────────┐
│              CASCADE SEARCH ENGINE                 │
│                (fetch_news.py)                    │
│                                                   │
│  Stage 1: Clean & normalize the query             │
│      │                                            │
│      ▼                                            │
│  Stage 2: GNews API  ──► Articles found? ──► ✅  │
│      │ (No)                                       │
│      ▼                                            │
│  Stage 3: Google News RSS ──► Articles? ──► ✅   │
│      │ (No)                                       │
│      ▼                                            │
│  Stage 4: DuckDuckGo News ──► Articles? ──► ✅   │
│      │ (No)                                       │
│      ▼                                            │
│  Stage 5: Gemini LLM pivots query → retry 2 & 3  │
└───────────────────────────────────────────────────┘
        │
        ▼ (Raw Articles)
┌───────────────────────────┐
│  TEXT PREPROCESSING       │
│  (preprocess.py)          │
│  · Lowercase              │
│  · Remove HTML/URLs       │
│  · Strip punctuation      │
│  · Remove stop words      │
└───────────────────────────┘
        │
        ▼ (Clean Text)
┌───────────────────────────────────────────────────┐
│              ANALYSIS ENGINE                       │
│                                                   │
│  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │  SENTIMENT ANALYSIS │  │   RISK SCORING      │ │
│  │  (sentiment.py)     │  │  (risk_score.py)    │ │
│  │  · VADER NLP model  │  │  · Neg. % weight    │ │
│  │  · Score: -1 to +1  │  │  · Alarming keywords│ │
│  │  · Positive/Neutral │  │  · Category counts  │ │
│  │    /Negative label  │  │  · Score: 0 to 100  │ │
│  └─────────────────────┘  └─────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │         EXECUTIVE SUMMARY (summarizer.py)   │  │
│  │  · Google Gemini 2.0 Flash LLM             │  │
│  │  · Fallback: NLTK extractive summarization │  │
│  └─────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────┐
│             VISUALIZATION LAYER                    │
│               (visualization.py + app.py)          │
│                                                   │
│  · KPI Cards (Articles, Sentiment %, Risk Score)  │
│  · AI Insight Box (auto-generated text alert)     │
│  · Sentiment Pie Chart (Plotly)                   │
│  · Risk Gauge (Plotly)                            │
│  · Source Distribution Bar Chart (Plotly)         │
│  · Sentiment by Source Stacked Bar (Plotly)       │
│  · Sentiment Timeline Scatter Plot (Plotly)       │
│  · Trending Keywords Word Cloud (Matplotlib)      │
│  · Top Keywords Bar Chart (Plotly)                │
│  · Full Article Feed with sentiment badges        │
│  · CSV Data Export                                │
└───────────────────────────────────────────────────┘
        │
        ▼
    Streamlit Web Dashboard (app.py)
```

---

## File Structure

```
AI_News_Intelligence_Dashboard/
│
├── app.py                      # Main Streamlit application — UI, routing, and chart rendering
│
├── requirements.txt            # All Python package dependencies
├── .gitignore                  # Excludes .env, __pycache__, venv, etc.
├── PROJECT_DOCS.md             # This file — full project documentation
│
├── .streamlit/
│   └── config.toml             # Forces global Light Mode theme for Streamlit widgets
│
├── .env                        # Secret API keys (NOT committed to GitHub)
│   ├── NEWS_API_KEY            # GNews.io API Key
│   └── GOOGLE_API_KEY          # Google AI Studio (Gemini) API Key
│
└── utils/                      # All backend logic — modular Python modules
    ├── fetch_news.py           # Cascade Search Engine — 5-stage multi-source fetcher + LLM pivot
    ├── preprocess.py           # Text cleaning — removes HTML, URLs, punctuation, stop words
    ├── sentiment.py            # VADER NLP sentiment classifier — returns label & score
    ├── risk_score.py           # Custom risk scoring algorithm — alarming keyword detection
    ├── summarizer.py           # AI Executive Summary — Gemini LLM with NLTK fallback
    └── visualization.py        # Reusable Plotly/Matplotlib chart factory functions
```

---

## Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Web Framework** | [Streamlit](https://streamlit.io/) | Full-stack interactive web dashboard |
| **Data Manipulation** | [Pandas](https://pandas.pydata.org/) | DataFrames, filtering, sorting, CSV export |
| **Visualization** | [Plotly](https://plotly.com/) | All interactive charts (pie, gauge, bar, scatter) |
| **Visualization** | [Matplotlib](https://matplotlib.org/) | Word Cloud rendering |
| **NLP / ML** | [NLTK (VADER)](https://www.nltk.org/) | Pre-trained sentiment analysis model |
| **Word Cloud** | [WordCloud](https://github.com/amueller/word_cloud) | Keyword frequency visualization |
| **AI / LLM** | [Google Gemini 2.0 Flash](https://ai.google.dev/) | Executive summaries + search query optimization |
| **HTTP Requests** | [Requests](https://requests.readthedocs.io/) | GNews API HTTP calls |
| **RSS Parsing** | [Feedparser](https://feedparser.readthedocs.io/) | Google News RSS feed parsing |
| **Web Search** | [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search) | Fallback news search engine |
| **Config** | [python-dotenv](https://pypi.org/project/python-dotenv/) | Loads API keys from .env locally |
| **Deployment** | [Render](https://render.com/) | Cloud platform hosting the live app |
| **Version Control** | [GitHub](https://github.com/) | Source code repository |

---

## Core Modules (utils/)

### `fetch_news.py` — The Cascade Search Engine
The most technically sophisticated module. Implements a 5-stage waterfall to maximize the chance of finding articles for **any** topic:

1. **Query Cleaning:** Strips junk words ("latest", "news", "today") that confuse exact-match APIs
2. **GNews API:** Primary source — structured, high-quality articles (requires API key)
3. **Google News RSS:** First fallback — free, no API key needed, uses `feedparser`
4. **DuckDuckGo News:** Second fallback — scrapes live news results with no rate limits
5. **LLM Query Pivot:** If all 3 sources return 0 results, **Gemini AI autonomously rewrites the search query** to something more searchable and retries stages 2 and 3

### `preprocess.py` — Text Cleaner
- Converts to lowercase
- Strips all HTML tags
- Removes URLs
- Removes punctuation and special characters
- Outputs clean normalized text for analysis

### `sentiment.py` — VADER Sentiment Classifier
- Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Returns a **compound score from -1.0 (most negative) to +1.0 (most positive)**
- Classification thresholds:
  - `≥ 0.05` → **Positive**
  - `≤ -0.05` → **Negative**
  - Between → **Neutral**
- Handles missing API keys gracefully (VADER is fully offline)

### `risk_score.py` — Risk Scoring Algorithm
Custom-engineered composite formula:
```
Risk Score = (Negative Article % × 0.6) + min(Alarming Word Count × 5, 40)
Final Score capped at 100
```
**Alarming word categories:**
- **Financial:** crisis, crash, bankrupt, plunge, collapse, recession, default...
- **Security:** scam, fraud, hack, breach, attack, emergency, threat, warning...
- **Legal/Other:** lawsuit, scandal, investigation, penalty, guilty, illegal...

### `summarizer.py` — AI Executive Summary Generator
- Primary: Sends article text to **Google Gemini 2.0 Flash** with a structured analytical prompt
- Fallback: If no API key or Gemini fails, uses **NLTK extractive summarization** (sentence scoring by word frequency)
- Truncates input to 800 words to stay within token limits

### `visualization.py` — Chart Factory
- `create_sentiment_pie_chart(df)` — Donut chart with Green/Amber/Red palette
- `create_risk_gauge(score)` — Gauge chart with animated needle
- `create_wordcloud(text)` — Matplotlib word cloud image

---

## Key Features

| Feature | Description |
|---|---|
| **5-Stage Cascade Fetcher** | Never shows "no results" — falls back across 3 sources + AI query rewriting |
| **Real-time Sentiment Classification** | VADER NLP model labels each article Positive / Neutral / Negative |
| **Custom Risk Scoring** | Proprietary 0–100 risk meter using negative % + alarming keyword detection |
| **AI Executive Summary** | Gemini 2.0 Flash generates a 1-paragraph analyst-style summary |
| **Sentiment Timeline** | Scatter plot showing how article sentiment moves across publication dates |
| **Source Breakdown** | Bar charts showing which publishers are contributing and with what tone |
| **Trending Keywords** | Word Cloud + Top 12 Keywords bar chart |
| **Filter & Sort News Feed** | Filter by sentiment; sort by date, positive-first, or negative-first |
| **CSV Export** | Download the full analyzed dataset as a spreadsheet |
| **Session State Persistence** | Results don't reset when interacting with sidebar filters |
| **Quick Topic Presets** | 8 pre-built topic buttons for instant one-click analysis |

---

## How It Works — Step by Step

1. **User enters a topic** (e.g., "Tesla earnings") in the search bar and clicks **Analyze**
2. `fetch_live_news()` runs the 5-stage cascade to find articles
3. Each article's text is cleaned by `clean_text()` in `preprocess.py`
4. `analyze_sentiment()` scores every article and assigns a label
5. `calculate_risk_score()` computes the composite risk number and category breakdown
6. `generate_executive_summary()` sends all article text to Gemini for a professional summary
7. The app renders all KPI cards, charts, and the article feed in the Streamlit UI
8. The user can filter, sort, explore, and download the data

---

## Setup & Local Run

### Prerequisites
- Python 3.9+
- A [GNews API Key](https://gnews.io/) (free tier: 100 requests/day, max 10 articles)
- A [Google Gemini API Key](https://aistudio.google.com/apikey) (free)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hemanth-sai-2203/ai-news-intelligence.git
cd ai-news-intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your environment file
echo NEWS_API_KEY=your_gnews_api_key_here > .env
echo GOOGLE_API_KEY=your_gemini_api_key_here >> .env

# 4. Run the application
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## Environment Variables

Create a `.env` file in the project root:

```env
# GNews API Key — https://gnews.io/
NEWS_API_KEY=your_gnews_api_key_here

# Google Gemini API Key — https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_gemini_api_key_here
```

> **Note:** The `.env` file is listed in `.gitignore` and will never be committed to GitHub.
> For deployment on Render, add these as **Environment Variables** in the Render dashboard.

---

## Deployment

This project is deployed on **[Render](https://render.com/)** as a Web Service.

**Render Configuration:**
| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT` |
| **Instance Type** | Free |

> **Note:** On the free tier, the server spins down after 15 minutes of inactivity. The first visit after inactivity may take ~50 seconds to wake up.

---

## Real-World Use Cases

| User | How They Use It |
|---|---|
| **Investors & Traders** | Monitor real-time sentiment on stocks, commodities, or markets before making decisions |
| **PR & Communications Teams** | Track how media is covering a brand or competitor; detect negative press cycles early |
| **Journalists & Researchers** | Analyze media bias, spot trending narratives, and identify keyword patterns across sources |
| **Risk Analysts** | Detect misinformation spikes and measure the intensity of crisis-level news coverage |
| **Students & Academics** | Study NLP, sentiment analysis, and LLM integration with a working, live project |

---

*Built with Python, Streamlit, Google Gemini, and NLTK.*
