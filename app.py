import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
from collections import Counter
import re
from utils.fetch_news import fetch_live_news
from utils.preprocess import clean_text
from utils.sentiment import analyze_sentiment
from utils.risk_score import calculate_risk_score
from utils.visualization import create_sentiment_pie_chart, create_risk_gauge, create_wordcloud
from utils.summarizer import generate_executive_summary

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
if 'app_data' not in st.session_state:
    st.session_state.app_data = None

st.set_page_config(
    page_title="AI News Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Clean SaaS background */
    .stApp {
        background: #f8fafc;
        color: #334155;
    }

    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #0f172a;
        font-weight: 600;
    }

    /* Hero banner */
    .hero-banner {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 32px 40px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .hero-banner h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 8px 0;
        font-family: 'Inter', sans-serif;
    }
    .hero-banner p {
        color: #475569;
        font-size: 1.05rem;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 16px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* KPI metric cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
        font-weight: 600;
    }
    .kpi-sub {
        font-size: 0.85rem;
        margin-top: 6px;
        color: #475569;
    }
    .positive { color: #16a34a; }
    .negative { color: #dc2626; }
    .neutral  { color: #d97706; }

    /* News article cards */
    .news-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-left: 4px solid #e2e8f0;
    }
    .card-positive { border-left-color: #22c55e; }
    .card-negative { border-left-color: #ef4444; }
    .card-neutral  { border-left-color: #f59e0b; }

    .news-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin: 0 0 8px 0;
        line-height: 1.4;
    }
    .news-meta {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin: 0 0 12px 0;
    }
    .news-meta span {
        font-size: 0.8rem;
        color: #64748b;
    }
    .news-description {
        font-size: 0.95rem;
        color: #334155;
        margin: 0 0 16px 0;
        line-height: 1.6;
    }
    .sentiment-badge {
        display: inline-block;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-positive { background: #dcfce7; color: #166534; }
    .badge-negative { background: #fee2e2; color: #991b1b; }
    .badge-neutral  { background: #fef3c7; color: #92400e; }

    /* Section headers */
    .section-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 40px 0 16px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 8px;
    }

    /* Risk level explanation */
    .risk-explanation {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 16px;
        margin-top: 16px;
        font-size: 0.85rem;
        color: #475569;
    }

    /* Insight Box */
    .insight-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 12px;
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.6;
    }

    /* Buttons */
    .stButton > button {
        background: #0f172a !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    .stButton > button:hover {
        background: #1e293b !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        color: #0f172a !important;
        border-radius: 6px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Dividers */
    hr { border-color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Control Panel")
    st.markdown("---")

    st.markdown("### Quick Topics")
    quick_topics = {
        "Custom Search...": "",
        "Artificial Intelligence": "Artificial Intelligence",
        "Bitcoin & Crypto": "Bitcoin crypto",
        "Climate Change": "Climate Change",
        "Healthcare": "Healthcare medicine",
        "Stock Market": "Stock Market economy",
        "Space Exploration": "NASA space",
        "US Politics": "US Politics",
        "Sports": "Sports",
    }

    selected_quick = st.radio("Select a topic:", list(quick_topics.keys()), label_visibility="collapsed")
    st.markdown("---")
    max_articles = st.slider("Number of articles", min_value=1, max_value=10, value=10, step=1)
    st.caption("*(GNews Free Tier limit is 10 articles)*")
    st.markdown("---")

    # About
    st.markdown("""
    ### How it works
    1. Fetches live news via GNews API
    2. Cleans text with NLP preprocessing
    3. Analyzes sentiment (Positive / Neutral / Negative)
    4. Calculates a risk score based on negative signals
    5. Visualizes trends, keywords & article breakdown
    """)

    st.markdown("---")
    st.markdown("### Real-World Use Cases")
    st.markdown("""
    - Investors track market sentiment
    - Journalists spot trending narratives
    - PR Teams monitor brand reputation
    - Researchers analyze media bias
    - Analysts detect misinformation spikes
    """)

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">LIVE INTELLIGENCE</div>
    <h1>AI News Intelligence Dashboard</h1>
    <p>Real-time news fetching, sentiment analysis, and risk scoring.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEARCH BAR
# ─────────────────────────────────────────────
col_search, col_btn = st.columns([5, 1])
with col_search:
    topic = st.text_input(
        "Search topic",
        value=quick_topics[selected_quick],
        placeholder="Enter any topic you wish to analyze...",
        label_visibility="collapsed"
    )
with col_btn:
    analyze_clicked = st.button("Analyze", use_container_width=True)

# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────
if analyze_clicked:
    if not topic.strip():
        st.warning("Please enter a topic to search.")
    else:
        with st.spinner(f"Fetching & analyzing live news for **{topic}**..."):
            articles, error_msg, metadata = fetch_live_news(topic, max_articles=max_articles)

        if error_msg:
            st.error(f"Error: {error_msg}")
        elif not articles:
            st.warning("No articles found even after multi-source cascade. The topic may be too obscure.")
        else:
            st.session_state.app_data = {
                'topic': topic,
                'articles': articles,
                'metadata': metadata
            }

if st.session_state.app_data is not None:
    topic = st.session_state.app_data['topic']
    articles = st.session_state.app_data['articles']
    metadata = st.session_state.app_data['metadata']

    if True:
        # Inform user if cascade/pivoting happened
        if metadata.get('pivoted'):
            st.info(f"✨ **AI Query Optimization:** Original search '{metadata['original']}' yielded 0 results. The AI autonomously expanded the search to **'{metadata['searched']}'** using **{metadata['source']}** to find these results.")
        elif metadata.get('source') and 'Fallback' in metadata.get('source', ''):
            st.info(f"🔄 **Cascade Fallback Engaged:** Switched to **{metadata['source']}** to bypass API limitations and find historical/real-time data for '{metadata['searched']}'.")

        # ── PROCESSING ──────────────────────────────
            processed_data = []
            all_text = ""
            raw_descriptions = ""
            
            for art in articles:
                title = art.get('title') or ''
                desc  = art.get('description') or ''
                content = f"{title}. {desc}"
                raw_descriptions += " " + content
                clean_content = clean_text(content)
                all_text += " " + clean_content
                sentiment_label, sentiment_score = analyze_sentiment(content)
                pub_raw = art.get('publishedAt', '')
                try:
                    pub_dt = datetime.fromisoformat(pub_raw.replace("Z", "+00:00"))
                    pub_str = pub_dt.strftime("%b %d, %Y · %H:%M UTC")
                    pub_date = pub_dt.strftime("%b %d")
                except:
                    pub_str = pub_raw
                    pub_date = pub_raw

                processed_data.append({
                    'title':       title,
                    'description': desc,
                    'source':      art.get('source', {}).get('name', 'Unknown'),
                    'url':         art.get('url', ''),
                    'publishedAt': pub_str,
                    'pub_date':    pub_date,
                    'sentiment':   sentiment_label,
                    'sentiment_score': round(sentiment_score, 2),
                    'image':       art.get('image', '')
                })

            df = pd.DataFrame(processed_data)
            risk_score, category_counts = calculate_risk_score(processed_data)
            total      = len(df)
            positive   = len(df[df['sentiment'] == 'Positive'])
            neutral    = len(df[df['sentiment'] == 'Neutral'])
            negative   = len(df[df['sentiment'] == 'Negative'])
            pos_pct    = round(positive / total * 100)
            neg_pct    = round(negative / total * 100)
            neu_pct    = round(neutral  / total * 100)

            # ── OVERALL MOOD ─────────────────────────────
            if pos_pct > 50:
                mood_label = "Predominantly Positive"
                mood_color = "positive"
            elif neg_pct > 40:
                mood_label = "Predominantly Negative"
                mood_color = "negative"
            else:
                mood_label = "Mixed / Neutral"
                mood_color = "neutral"

            # ── KPI CARDS ─────────────────────────────────
            st.markdown(f'<div class="section-header">SNAPSHOT — Topic: {topic.upper()}</div>', unsafe_allow_html=True)
            k1, k2, k3, k4, k5 = st.columns(5)

            with k1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{total}</div>
                    <div class="kpi-label">Articles Analyzed</div>
                    <div class="kpi-sub" style="color:#94a3b8">Live news fetched</div>
                </div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value positive">{pos_pct}%</div>
                    <div class="kpi-label">Positive Coverage</div>
                    <div class="kpi-sub positive">{positive} articles</div>
                </div>""", unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value negative">{neg_pct}%</div>
                    <div class="kpi-label">Negative Coverage</div>
                    <div class="kpi-sub negative">{negative} articles</div>
                </div>""", unsafe_allow_html=True)
            with k4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value neutral">{neu_pct}%</div>
                    <div class="kpi-label">Neutral Coverage</div>
                    <div class="kpi-sub neutral">{neutral} articles</div>
                </div>""", unsafe_allow_html=True)
            with k5:
                risk_color = "#68d391" if risk_score < 30 else ("#f6ad55" if risk_score < 70 else "#fc8181")
                risk_label = "LOW RISK" if risk_score < 30 else ("MODERATE" if risk_score < 70 else "HIGH RISK")
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value" style="color:{risk_color}">{risk_score:.0f}/100</div>
                    <div class="kpi-label">Risk Score</div>
                    <div class="kpi-sub" style="color:{risk_color}">{risk_label}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── AI INSIGHT BOX ─────────────────────────────
            if neg_pct > 50:
                insight = f"High Alert: Over {neg_pct}% of news coverage about **{topic}** is negative. This may indicate market volatility, a PR crisis, or a major negative event. Investors and stakeholders should monitor closely."
            elif pos_pct > 60:
                insight = f"Bullish Signal: {pos_pct}% of coverage is positive — media sentiment around **{topic}** is strong. This is often associated with growing public interest, good news cycles, or positive industry developments."
            elif risk_score > 70:
                insight = f"Risk Alert: The risk score of {risk_score:.0f}/100 is HIGH for **{topic}**. Multiple alarming keywords detected across articles. This suggests potential misinformation, crisis coverage, or public controversy."
            else:
                insight = f"Balanced Coverage: News sentiment about **{topic}** is relatively balanced ({pos_pct}% positive, {neg_pct}% negative). No major sentiment extremes detected — this is typical for ongoing, stable topics."

            st.markdown(f'<div class="insight-box"><strong>Insight Analysis:</strong> {insight}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # ── EXECUTIVE SUMMARY ────────────────────────
            st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
            with st.spinner("Generating executive summary..."):
                exec_summary = generate_executive_summary(raw_descriptions)
                
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; font-size: 1.05rem; color: #334155; line-height: 1.7;">
                {exec_summary}
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Data (CSV)",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{topic}_intelligence_report.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── CHARTS ROW 1 ──────────────────────────────
            st.markdown('<div class="section-header">Sentiment & Risk Analysis</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)

            with c1:
                pie_fig = create_sentiment_pie_chart(df)
                if pie_fig:
                    pie_fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#334155'),
                        legend=dict(font=dict(color='#475569'))
                    )
                    st.plotly_chart(pie_fig, use_container_width=True)
                st.markdown(f"""
                <div class="risk-explanation">
                    <strong>What this means:</strong> Sentiment analysis uses NLP to classify each article's tone.
                    A high Positive ratio signals good news cycles.
                    A high Negative ratio warrants closer attention.
                </div>""", unsafe_allow_html=True)

            with c2:
                gauge_fig = create_risk_gauge(risk_score)
                gauge_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#334155')
                )
                st.plotly_chart(gauge_fig, use_container_width=True)
                st.markdown(f"""
                <div class="risk-explanation">
                    <strong>Risk Score Explained:</strong><br>
                    0–30 Low — Mostly factual, calm reporting<br>
                    31–70 Moderate — Mixed signals, monitor trends<br>
                    71–100 High — Crisis-level negativity or alarming language detected<br>
                    <hr style="margin: 8px 0; border-color: #e2e8f0;">
                    <strong>Risk Categories Detected:</strong><br>
                    Financial: {category_counts.get('Financial', 0)} | Security: {category_counts.get('Security', 0)} | Legal/Other: {category_counts.get('Legal/Other', 0)}
                </div>""", unsafe_allow_html=True)

            # ── SOURCE BREAKDOWN ──────────────────────────
            st.markdown('<div class="section-header">SOURCE DISTRIBUTION & TIMELINE</div>', unsafe_allow_html=True)
            c3, c4 = st.columns(2)

            with c3:
                source_counts = df['source'].value_counts().reset_index()
                source_counts.columns = ['Source', 'Articles']
                bar_fig = px.bar(
                    source_counts,
                    x='Articles', y='Source',
                    orientation='h',
                    color='Articles',
                    color_continuous_scale=['#bfdbfe', '#2563eb'],
                    title="Articles by News Source"
                )
                bar_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#334155'),
                    title_font=dict(color='#0f172a'),
                    showlegend=False,
                    coloraxis_showscale=False,
                    yaxis=dict(gridcolor='#e2e8f0'),
                    xaxis=dict(gridcolor='#e2e8f0')
                )
                st.plotly_chart(bar_fig, use_container_width=True)

            with c4:
                sentiment_by_source = df.groupby(['source', 'sentiment']).size().reset_index(name='count')
                color_map = {'Positive': '#22c55e', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
                stacked = px.bar(
                    sentiment_by_source,
                    x='source', y='count', color='sentiment',
                    color_discrete_map=color_map,
                    title="Sentiment Breakdown by Source",
                    barmode='stack'
                )
                stacked.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#334155'),
                    title_font=dict(color='#0f172a'),
                    legend=dict(font=dict(color='#475569')),
                    xaxis=dict(gridcolor='#e2e8f0', tickangle=-30),
                    yaxis=dict(gridcolor='#e2e8f0')
                )
                st.plotly_chart(stacked, use_container_width=True)

            # ── WORD CLOUD ────────────────────────────────
            st.markdown('<div class="section-header">TRENDING KEYWORDS</div>', unsafe_allow_html=True)
            c5, c6 = st.columns([2, 1])

            with c5:
                wc_fig = create_wordcloud(all_text)
                if wc_fig:
                    st.pyplot(wc_fig)

            with c6:
                # Top keywords as bar
                words = [w for w in all_text.split() if len(w) > 3]
                word_freq = Counter(words).most_common(12)
                if word_freq:
                    wf_df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])
                    wf_fig = px.bar(
                        wf_df, x='Frequency', y='Word',
                        orientation='h',
                        color='Frequency',
                        color_continuous_scale=['#e0e7ff', '#4f46e5'],
                        title="Top 12 Keywords"
                    )
                    wf_fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#334155'),
                        title_font=dict(color='#0f172a'),
                        showlegend=False,
                        coloraxis_showscale=False,
                        yaxis=dict(gridcolor='#e2e8f0'),
                        xaxis=dict(gridcolor='#e2e8f0')
                    )
                    st.plotly_chart(wf_fig, use_container_width=True)

            # ── SENTIMENT TIMELINE ───────────────────────
            st.markdown('<div class="section-header">Sentiment Timeline</div>', unsafe_allow_html=True)

            timeline_df = df[['publishedAt', 'sentiment_score', 'sentiment', 'title']].copy()
            # Only render if we have at least 2 distinct dates; otherwise show a note
            unique_dates = timeline_df['publishedAt'].nunique()
            if unique_dates < 2:
                st.markdown("""
                <div class="risk-explanation">
                    <strong>Note:</strong> All fetched articles were published on the same date/time,
                    so a timeline chart is not meaningful. Try searching a broader topic to get
                    articles spanning multiple days.
                </div>""", unsafe_allow_html=True)
            else:
                timeline_df = timeline_df.sort_values('publishedAt')
                color_map_tl = {'Positive': '#22c55e', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
                tl_fig = px.scatter(
                    timeline_df,
                    x='publishedAt',
                    y='sentiment_score',
                    color='sentiment',
                    color_discrete_map=color_map_tl,
                    hover_data={'title': True, 'sentiment_score': ':.2f', 'sentiment': True, 'publishedAt': False},
                    title='Sentiment Score Over Time  (hover dots to read headline)',
                    labels={'publishedAt': 'Published Date', 'sentiment_score': 'Sentiment Score (-1 to +1)'}
                )
                # Add a smoothed trend line via a separate scatter with lines
                tl_fig.add_scatter(
                    x=timeline_df['publishedAt'],
                    y=timeline_df['sentiment_score'],
                    mode='lines',
                    line=dict(color='#94a3b8', width=1.5, dash='dot'),
                    showlegend=False,
                    hoverinfo='skip'
                )
                # Add a zero baseline
                tl_fig.add_hline(
                    y=0,
                    line_dash='dash',
                    line_color='#cbd5e1',
                    annotation_text='Neutral baseline',
                    annotation_position='bottom right',
                    annotation_font_color='#94a3b8'
                )
                tl_fig.update_traces(marker=dict(size=12), selector=dict(mode='markers'))
                tl_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#334155'),
                    title_font=dict(color='#0f172a', size=14),
                    legend=dict(font=dict(color='#475569'), title_text='Sentiment'),
                    xaxis=dict(gridcolor='#e2e8f0', tickangle=-30),
                    yaxis=dict(gridcolor='#e2e8f0', range=[-1.1, 1.1], zeroline=False),
                    height=380
                )
                st.plotly_chart(tl_fig, use_container_width=True)
                st.markdown("""
                <div class="risk-explanation">
                    <strong>How to read this:</strong> Each dot represents one article.
                    Scores above 0 indicate positive tone; below 0 indicate negative tone.
                    A downward trend over time suggests worsening media sentiment on this topic.
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── NEWS FEED ──────────────────────────────
            st.markdown('<div class="section-header">Detailed News Feed</div>', unsafe_allow_html=True)

            # Filter controls
            f1, f2 = st.columns([3, 1])
            with f1:
                sentiment_filter = st.multiselect(
                    "Filter by sentiment:",
                    ["Positive", "Neutral", "Negative"],
                    default=["Positive", "Neutral", "Negative"]
                )
            with f2:
                sort_by = st.selectbox("Sort by:", ["Latest First", "Positive First", "Negative First"])

            filtered_df = df[df['sentiment'].isin(sentiment_filter)]
            if sort_by == "Positive First":
                order = ["Positive", "Neutral", "Negative"]
                filtered_df = filtered_df.assign(
                    _order=filtered_df['sentiment'].map({s: i for i, s in enumerate(order)})
                ).sort_values('_order')
            elif sort_by == "Negative First":
                order = ["Negative", "Neutral", "Positive"]
                filtered_df = filtered_df.assign(
                    _order=filtered_df['sentiment'].map({s: i for i, s in enumerate(order)})
                ).sort_values('_order')

            for _, row in filtered_df.iterrows():
                badge_class = f"badge-{row['sentiment'].lower()}"
                card_class  = f"card-{row['sentiment'].lower()}"
                emoji = "✅" if row['sentiment'] == 'Positive' else ("❌" if row['sentiment'] == 'Negative' else "➖")

                st.markdown(f"""
                <div class="news-card {card_class}">
                    <div class="news-title">{row['title']}</div>
                    <div class="news-meta">
                        <span>📰 {row['source']}</span>
                        <span>🕒 {row['publishedAt']}</span>
                        <span class="sentiment-badge {badge_class}">{emoji} {row['sentiment']} (Score: {row['sentiment_score']})</span>
                    </div>
                    <div class="news-description">{row['description']}</div>
                    <a href="{row['url']}" target="_blank" style="
                        display:inline-block;
                        margin-left: 8px;
                        font-size: 0.82rem;
                        color: #2563eb;
                        text-decoration: none;
                        font-weight: 500;
                        border: 1px solid #bfdbfe;
                        padding: 4px 14px;
                        border-radius: 20px;
                        transition: background 0.2s;">
                        🔗 Read Full Article →
                    </a>
                </div>""", unsafe_allow_html=True)

            # ── DATA TABLE ────────────────────────────────
            with st.expander("📋 Export Raw Data Table"):
                export_df = df[['title', 'source', 'publishedAt', 'sentiment', 'url']].copy()
                export_df.columns = ['Title', 'Source', 'Published At', 'Sentiment', 'URL']
                st.dataframe(export_df, use_container_width=True)
                csv = export_df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", csv, f"news_{topic.replace(' ', '_')}.csv", "text/csv")

else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 0 40px;">
        <div style="font-size: 5rem; margin-bottom: 16px;">🧠</div>
        <h2 style="color:#0f172a; font-weight:600; margin-bottom:12px;">Choose a topic and click Analyze</h2>
        <p style="color:#64748b; font-size:1.1rem; max-width:600px; margin: 0 auto;">
            The dashboard will fetch live news articles, run NLP sentiment analysis, 
            calculate a risk score and generate keyword intelligence — all in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uc1, uc2, uc3 = st.columns(3)
    use_cases = [
        ("📈", "Investors & Traders", "Track market sentiment in real-time. Know when fear or greed dominates a topic before making decisions."),
        ("🏢", "PR & Brand Monitoring", "Monitor how the media is covering your brand or competitors. Detect negative press early."),
        ("🔬", "Research & Journalism", "Identify trending narratives, detect media bias, and analyze keyword patterns across sources."),
    ]
    for col, (icon, title, desc) in zip([uc1, uc2, uc3], use_cases):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; padding: 28px;">
                <div style="font-size:2.5rem; margin-bottom:12px;">{icon}</div>
                <div style="font-size:1rem; font-weight:600; color:#0f172a; margin-bottom:10px;">{title}</div>
                <div style="font-size:0.88rem; color:#64748b; line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)
