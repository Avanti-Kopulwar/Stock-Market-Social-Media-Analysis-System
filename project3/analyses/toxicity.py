import pandas as pd
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
from utils.db_postgres import get_postgres_connection
import json

def get_toxicity_trends():
    conn = get_postgres_connection()

    reddit_query = """
        SELECT post_date::date AS date, AVG(toxicity_score) AS avg_toxicity
        FROM sentiment_toxicity_logs
        WHERE platform = 'reddit'
        GROUP BY date
        ORDER BY date;
    """

    chan_query = """
        SELECT post_date::date AS date, AVG(toxicity_score) AS avg_toxicity
        FROM sentiment_toxicity_logs
        WHERE platform = 'chan'
          AND post_date >= '2025-01-01'
          AND post_date <  '2026-01-01'
        GROUP BY date
        ORDER BY date;
    """

    reddit_df = pd.read_sql(reddit_query, conn)
    chan_df   = pd.read_sql(chan_query, conn)
    conn.close()

    # Scale avg toxicity
    if not reddit_df.empty:
        reddit_df["avg_toxicity"] *= 100
    if not chan_df.empty:
        chan_df["avg_toxicity"] *= 100

    # Reddit figure
    reddit_fig = go.Figure(
        data=[
            go.Scatter(
                x=reddit_df["date"],
                y=reddit_df["avg_toxicity"],
                mode="lines+markers",
                line=dict(color="#00b4ff", width=3)
            )
        ]
    )
    reddit_fig.update_layout(
        title="Reddit Toxicity Over Time",
        template="plotly_dark"
    )

    # /pol/ figure
    chan_fig = go.Figure(
        data=[
            go.Scatter(
                x=chan_df["date"],
                y=chan_df["avg_toxicity"],
                mode="lines+markers",
                line=dict(color="#ff5733", width=3)
            )
        ]
    )
    chan_fig.update_layout(
        title="/pol/ Toxicity in 2025",
        template="plotly_dark"
    )

    # **THE IMPORTANT PART**
    return {
        "reddit_plot": json.dumps(reddit_fig, cls=PlotlyJSONEncoder),
        "chan_plot": json.dumps(chan_fig, cls=PlotlyJSONEncoder)
    }