import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")

# --- Connect to PostgreSQL ---
conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"  # replace if needed
)
logging.info("Connected to PostgreSQL successfully.")

# --- SQL Query ---
query = """
WITH metrics AS (
    SELECT
        'Reddit' AS platform,
        COUNT(*) AS total_posts,
        ROUND(AVG(sentiment_score)::numeric, 3) AS avg_sentiment,
        ROUND(AVG(toxicity_score)::numeric, 3) AS avg_toxicity,
        MIN(post_date) AS start_date,
        MAX(post_date) AS end_date
    FROM sentiment_toxicity_logs
    WHERE platform = 'reddit'

    UNION ALL

    SELECT
        '4chan (/pol/)' AS platform,
        COUNT(*) AS total_posts,
        ROUND(AVG(sentiment_score)::numeric, 3) AS avg_sentiment,
        ROUND(AVG(toxicity_score)::numeric, 3) AS avg_toxicity,
        MIN(post_date) AS start_date,
        MAX(post_date) AS end_date
    FROM sentiment_toxicity_logs
    WHERE platform = '4chan'
)
SELECT * FROM metrics;
"""

df = pd.read_sql_query(query, conn)
conn.close()

# --- Format date range column ---
df["Date Range"] = df.apply(lambda x: f"{x['start_date']:%b}–{x['end_date']:%b %Y}", axis=1)
df = df.drop(columns=["start_date", "end_date"])

# --- Rename columns for cleaner display ---
df.rename(columns={
    "platform": "Platform",
    "total_posts": "Total Posts",
    "avg_sentiment": "Avg Sentiment",
    "avg_toxicity": "Avg Toxicity"
}, inplace=True)

# --- Create the matplotlib table ---
fig, ax = plt.subplots(figsize=(8, 2.2))
ax.axis("off")

tbl = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc="center",
    loc="center"
)

tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.5)

# --- Style header row ---
for key, cell in tbl.get_celld().items():
    if key[0] == 0:
        cell.set_text_props(weight='bold')
        cell.set_facecolor('#D9EAF7')

plt.title("Table 1 – Dataset Summary Across Platforms", fontsize=12, pad=15, weight='bold')

plt.tight_layout()
plt.savefig("dataset_summary_table.png", dpi=300)
plt.close()

logging.info(" Saved dataset_summary_table.png successfully.")