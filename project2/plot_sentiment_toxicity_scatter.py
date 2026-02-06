
"""
Figure 5 – Sentiment vs Toxicity Scatterplot
Compares sentiment (x-axis) and toxicity (y-axis) for Reddit and 4chan (/pol/).
Each point represents one post from sentiment_toxicity_logs.
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")
logging.info("Generating Figure 5 – Sentiment vs Toxicity Scatterplot")


conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"   
)

query = """
SELECT platform, sentiment_score, toxicity_score
FROM sentiment_toxicity_logs
WHERE sentiment_score IS NOT NULL
  AND toxicity_score IS NOT NULL
  AND platform IN ('reddit', '4chan')
  AND post_date >= '2025-09-01';
"""

df = pd.read_sql_query(query, conn)
conn.close()
logging.info(f"Loaded {len(df)} sentiment–toxicity records.")

plt.figure(figsize=(9, 6))
plt.scatter(
    df.loc[df["platform"] == "reddit", "sentiment_score"],
    df.loc[df["platform"] == "reddit", "toxicity_score"],
    color="orange", alpha=0.3, s=10, label="Reddit"
)

plt.scatter(
    df.loc[df["platform"] == "4chan", "sentiment_score"],
    df.loc[df["platform"] == "4chan", "toxicity_score"],
    color="blue", alpha=0.3, s=10, label="/pol/ (4chan)"
)

plt.title("Figure 5 – Sentiment vs Toxicity Scatterplot (Sept–Dec 2025)", fontsize=14, pad=15)
plt.xlabel("Sentiment Score (VADER Compound)", fontsize=12)
plt.ylabel("Toxicity Score (0–1, Perspective API)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Platform")
plt.tight_layout()

output_path = "figure5_sentiment_toxicity_scatter.png"
plt.savefig(output_path, dpi=300)
plt.close()
logging.info(f"Saved Figure 5 as {output_path}")