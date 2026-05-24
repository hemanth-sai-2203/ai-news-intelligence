import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def create_sentiment_pie_chart(df):
    if df.empty:
        return None
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    color_discrete_map = {'Positive': '#22c55e', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
    fig = px.pie(sentiment_counts, names='Sentiment', values='Count', 
                 color='Sentiment', color_discrete_map=color_discrete_map,
                 title='Sentiment Distribution')
    return fig

def create_risk_gauge(risk_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Misinformation & Risk Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#0f172a"},
            'steps' : [
                {'range': [0, 30], 'color': "#22c55e"},
                {'range': [30, 70], 'color': "#f59e0b"},
                {'range': [70, 100], 'color': "#ef4444"}],
            'threshold' : {
                'line': {'color': "#7f1d1d", 'width': 4},
                'thickness': 0.75,
                'value': 90}
        }
    ))
    return fig

def create_wordcloud(text):
    if not text.strip():
        return None
    wordcloud = WordCloud(
        width=900, height=380,
        background_color='#ffffff',
        colormap='Blues',
        prefer_horizontal=0.8,
        max_words=80,
        contour_width=0,
        font_step=1
    ).generate(text)
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig
