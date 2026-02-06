import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

# ---------------- CONFIG ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
DB_CONFIG = {
    "dbname": "social_media",
    "user": "sjadhav",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

logging.info("Generating Figure 2 – Sentiment Distribution Across Platforms")

# ---------------- FETCH DATA ----------------
conn = psycopg2.connect(**DB_CONFIG)
query = """
SELECT platform, sentiment_score
FROM sentiment_toxicity_logs
WHERE sentiment_score IS NOT NULL
  AND platform IN ('reddit', '4chan');
"""
df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    logging.warning("No sentiment data found.")
else:
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x="sentiment_score", hue="platform", fill=True, common_norm=False, alpha=0.5)
    plt.title("Figure 2 – Sentiment Distribution Across Platforms", fontsize=14, fontweight="bold")
    plt.xlabel("Sentiment Score (VADER Compound)", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("figure2_sentiment_distribution.png", dpi=300)
    logging.info("Saved plot as figure2_sentiment_distribution.png")