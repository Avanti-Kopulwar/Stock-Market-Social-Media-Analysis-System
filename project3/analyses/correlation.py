import pandas as pd
import plotly.graph_objs as go
from scipy.stats import pearsonr
from utils.db_postgres import get_postgres_connection

# --------------------------------------------------
# SAFE CORR
# --------------------------------------------------
def safe_corr(x, y):
    if len(x) > 1 and len(y) > 1:
        try:
            return round(pearsonr(x, y)[0], 3)
        except:
            return None
    return None

# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------
def get_correlation_data():
    conn = get_postgres_connection()

    # ALWAYS USE DAILY AVERAGES — NOT RAW ROWS
    query_reddit = """
        SELECT post_date::date AS date,
               AVG(sentiment_score) AS sentiment,
               AVG(toxicity_score) AS toxicity
        FROM sentiment_toxicity_logs
        WHERE platform='reddit'
          AND sentiment_score IS NOT NULL
          AND toxicity_score IS NOT NULL
        GROUP BY 1
        ORDER BY 1;
    """

    query_chan = """
        SELECT post_date::date AS date,
               AVG(sentiment_score) AS sentiment,
               AVG(toxicity_score) AS toxicity
        FROM sentiment_toxicity_logs
        WHERE platform='chan'
          AND sentiment_score IS NOT NULL
          AND toxicity_score IS NOT NULL
        GROUP BY 1
        ORDER BY 1;
    """

    reddit = pd.read_sql(query_reddit, conn)
    chan = pd.read_sql(query_chan, conn)
    conn.close()

    # CORRELATION (if at least 2 points exist)
    reddit_corr = safe_corr(reddit["sentiment"], reddit["toxicity"])
    chan_corr = safe_corr(chan["sentiment"], chan["toxicity"])

    # --------------------------------------------------
    # REDDIT FIG — ONLY daily averages, ONLY 3 dots
    # --------------------------------------------------
    reddit_fig = go.Figure()

    if len(reddit) > 0:
        reddit_fig.add_trace(go.Scatter(
            x=reddit["sentiment"],
            y=reddit["toxicity"],
            mode="lines+markers",
            line=dict(color="#00b4ff", width=3),
            marker=dict(size=10)
        ))
    else:
        reddit_fig.add_annotation(text="NO DATA", showarrow=False)

    reddit_fig.update_layout(
        title=f"Reddit Sentiment vs Toxicity (r = {reddit_corr})",
        xaxis_title="Daily Avg Sentiment",
        yaxis_title="Daily Avg Toxicity",
        template="plotly_dark",
        height=450
    )

    # --------------------------------------------------
    # CHAN FIG
    # --------------------------------------------------
    chan_fig = go.Figure()

    if len(chan) > 0:
        chan_fig.add_trace(go.Scatter(
            x=chan["sentiment"],
            y=chan["toxicity"],
            mode="lines+markers",
            line=dict(color="#ff5733", width=3),
            marker=dict(size=10)
        ))
    else:
        chan_fig.add_annotation(text="NO DATA", showarrow=False)

    chan_fig.update_layout(
        title=f"/pol/ Sentiment vs Toxicity (r = {chan_corr})",
        xaxis_title="Daily Avg Sentiment",
        yaxis_title="Daily Avg Toxicity",
        template="plotly_dark",
        height=450
    )

    return reddit_fig, chan_fig, reddit_corr, chan_corr