import re
import pandas as pd
import plotly.graph_objs as go
from utils.db_postgres import get_postgres_connection

TICKER_REGEX = r'\b[A-Z]{2,5}\b'
BLACKLIST = {"THE", "AND", "ARE", "FOR", "YOU", "THIS", "THAT", "WITH"}

def extract_tickers(text):
    if not text:
        return []
    tickers = re.findall(TICKER_REGEX, text)
    return [t for t in tickers if t not in BLACKLIST]

def get_stock_mentions():
    conn = get_postgres_connection()

    query = """
        SELECT title, body, created_utc
        FROM reddit_posts
        WHERE created_utc >= '2025-01-01'
          AND created_utc <= '2025-12-31';
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df["text"] = df["title"].fillna("") + " " + df["body"].fillna("")
    df["tickers"] = df["text"].apply(extract_tickers)

    exploded = df.explode("tickers")
    exploded = exploded.dropna(subset=["tickers"])

    if exploded.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No stock mentions found in dataset.",
            showarrow=False,
            font=dict(color="orange", size=18)
        )
        fig.update_layout(
            template="plotly_dark",
            title="Stock Mentions (No Data)"
        )
        return fig

    counts = exploded["tickers"].value_counts().head(20)

    fig = go.Figure(
        data=[
            go.Bar(
                x=counts.index.tolist(),
                y=counts.values.tolist(),
                marker=dict(color="#00ff99")
            )
        ]
    )

    fig.update_layout(
        title="Top Mentioned Stocks on Reddit (2025)",
        xaxis_title="Ticker Symbol",
        yaxis_title="Frequency",
        template="plotly_dark"
    )

    return fig