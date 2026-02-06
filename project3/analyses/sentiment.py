import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.db_postgres import get_postgres_connection
import plotly.graph_objs as go

analyzer = SentimentIntensityAnalyzer()

def compute_sentiment(text):
    if not text or text.strip() == "":
        return "neutral"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def get_sentiment_trends():
    conn = get_postgres_connection()

    reddit_query = """
        SELECT created_utc, title, body
        FROM reddit_posts
        WHERE created_utc >= '2025-01-01'
          AND created_utc < '2026-01-01';
    """
    reddit_df = pd.read_sql(reddit_query, conn)
    reddit_df["text"] = reddit_df["title"].fillna("") + " " + reddit_df["body"].fillna("")
    reddit_df["sentiment"] = reddit_df["text"].apply(compute_sentiment)
    reddit_counts = reddit_df["sentiment"].value_counts().reindex(
        ["positive", "neutral", "negative"], fill_value=0
    )

    chan_query = """
        SELECT created_utc, comment AS body
        FROM chan_posts
        WHERE board = 'pol'
          AND (
                (created_utc BETWEEN '2025-10-13' AND '2025-10-31')
             OR (created_utc BETWEEN '2025-11-24' AND '2025-11-30')
          );
    """
    chan_df = pd.read_sql(chan_query, conn)
    chan_df["sentiment"] = chan_df["body"].fillna("").apply(compute_sentiment)
    chan_counts = chan_df["sentiment"].value_counts().reindex(
        ["positive", "neutral", "negative"], fill_value=0
    )

    conn.close()

    reddit_fig = go.Figure(
        data=[
            go.Pie(
                labels=["Positive", "Neutral", "Negative"],
                values=reddit_counts.values.tolist(),
                marker=dict(colors=["#2ecc71", "#f1c40f", "#e74c3c"])
            )
        ]
    )
    reddit_fig.update_layout(
        title="Reddit Sentiment Distribution (2025)",
        template="plotly_dark"
    )

    chan_fig = go.Figure(
        data=[
            go.Pie(
                labels=["Positive", "Neutral", "Negative"],
                values=chan_counts.values.tolist(),
                marker=dict(colors=["#2ecc71", "#f1c40f", "#e74c3c"])
            )
        ]
    )
    chan_fig.update_layout(
        title="/pol/ Sentiment Distribution (Oct 13–31 & Nov 24–30, 2025)",
        template="plotly_dark"
    )

    return {
        "reddit_fig": reddit_fig,
        "chan_fig": chan_fig
    }