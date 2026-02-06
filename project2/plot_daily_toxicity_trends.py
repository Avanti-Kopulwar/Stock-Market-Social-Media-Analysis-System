#!/usr/bin/env python3
"""
Figure 4 – Daily Average Toxicity Over Time
Plots day-wise mean toxicity for Reddit and 4chan /pol/
using Perspective API results from sentiment_toxicity_logs.
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import logging

# -------------------------------------------------------------
# Logging
# -------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [INFO] %(message)s"
)
logging.info("Generating Figure 4 – Daily Average Toxicity Over Time")

# -------------------------------------------------------------
# PostgreSQL connection
# -------------------------------------------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"   # change if needed
)

# -------------------------------------------------------------
# Query: daily average toxicity per platform
# -------------------------------------------------------------
query = """
SELECT
    DATE(post_date) AS day,
    platform,
    ROUND(AVG(toxicity_score)::numeric, 4) AS avg_toxicity
FROM sentiment_toxicity_logs
WHERE toxicity_score IS NOT NULL
  AND platform IN ('reddit', '4chan')
  AND post_date >= '2025-09-01'
GROUP BY 1, 2
ORDER BY 1;
"""

df = pd.read_sql_query(query, conn)
conn.close()
logging.info(f"Loaded {len(df)} daily toxicity records.")

# -------------------------------------------------------------
# Pivot + plot
# -------------------------------------------------------------
pivot_df = df.pivot(index="day", columns="platform", values="avg_toxicity").fillna(0)

plt.figure(figsize=(10, 6))
plt.plot(pivot_df.index, pivot_df["reddit"], color="orange", label="Reddit", linewidth=2)
plt.plot(pivot_df.index, pivot_df["4chan"], color="blue", label="/pol/ (4chan)", linewidth=2)

plt.title("Figure 4 – Daily Average Toxicity Over Time (Sept–Dec 2025)", fontsize=14, pad=15)
plt.xlabel("Date (Month–Day, 2025)", fontsize=12)
plt.ylabel("Average Toxicity (0–1)", fontsize=12)
plt.legend(title="Platform")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# -------------------------------------------------------------
# Save figure
# -------------------------------------------------------------
output_path = "figure4_daily_toxicity_trends.png"
plt.savefig(output_path, dpi=300)
plt.close()
logging.info(f"Saved Figure 4 as {output_path}")