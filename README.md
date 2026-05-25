# AI News Intelligence & Sentiment Analytics Dashboard

**🚀 Live Application:** [View the Dashboard on Render](https://ai-news-intelligence-5old.onrender.com)

A real-time AI-powered news intelligence dashboard using NLP, sentiment analysis, and interactive visualization techniques.

## Features
- Topic-based live news search via GNews API
- Positive/Negative/Neutral sentiment classification using VADER
- News Risk Meter (Misinformation scoring based on negative sentiment and alarming keywords)
- Trending Keyword Analytics and Word Cloud generation
- Interactive Plotly charts (Sentiment Distribution, Risk Gauge)

## Setup Instructions

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your GNews API Key:
   ```
   NEWS_API_KEY=your_api_key_here
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Folder Structure
- `app.py`: Main Streamlit application
- `utils/`: Contains modules for fetching news, preprocessing, sentiment analysis, and visualizations
- `data/`, `models/`, `assets/`, `screenshots/`: Directories for future usage and media

## Deployment
This project is ready to be deployed on Streamlit Community Cloud or Render.
