import pandas as pd
import plotly.graph_objs as go
from utils.db_postgres import get_postgres_connection

def get_activity_trend(platform, start_date, end_date):
    conn = get_postgres_connection()

    table = "reddit_posts" if platform == "reddit" else "chan_posts"

    query = f"""
        SELECT DATE(created_utc) AS date, COUNT(*) AS posts
        FROM {table}
        WHERE created_utc BETWEEN %s AND %s
        GROUP BY DATE(created_utc)
        ORDER BY DATE(created_utc);
    """

    df = pd.read_sql(query, conn, params=(start_date, end_date))
    conn.close()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["posts"] = df["posts"].astype(int)

    if platform == "reddit":
        df = df[(df["date"] >= pd.Timestamp("2025-10-01")) &
                (df["date"] <= pd.Timestamp("2026-12-31"))]

    elif platform == "chan":
        df = df[(df["date"] >= pd.Timestamp("2025-10-01")) &
                (df["date"] <= pd.Timestamp("2025-12-31"))]

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"No data available for {platform}",
            template="plotly_dark",
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font=dict(color="#c9d1d9")
        )
        return fig

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["posts"],
        mode="lines+markers",
        line=dict(color="#00b4ff", width=3),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f"Posting Activity: {platform.capitalize()}",
        xaxis_title="Date",
        yaxis_title="Post Count",
        template="plotly_dark",
        height=550
    )

    return fig