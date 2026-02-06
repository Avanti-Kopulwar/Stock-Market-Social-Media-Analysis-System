#!/usr/bin/env python3
"""
Figure 3 – Toxicity Distribution (Perspective API)
Generates a KDE + histogram plot comparing toxicity scores
for Reddit vs 4chan /pol/ based on Perspective API results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import logging

# ------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [INFO] %(message)s"
)
logging.info("Generating Figure 3 – Toxicity Distribution (Perspective API)")

# ------------------------------------------------------------------
# Connect to PostgreSQL
# ------------------------------------------------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"   # change if needed
)

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
query = """
SELECT platform, toxicity_score
FROM sentiment_toxicity_logs
WHERE toxicity_score IS NOT NULL
  AND platform IN ('reddit', '4chan')
"""
df = pd.read_sql_query(query, conn)

conn.close()
logging.info(f"Loaded {len(df)} rows for toxicity distribution plot.")

# ------------------------------------------------------------------
# Plot configuration
# ------------------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x="toxicity_score", hue="platform",
            fill=True, common_norm=False, alpha=0.4, linewidth=2)
sns.histplot(data=df, x="toxicity_score", hue="platform",
             bins=40, element="step", stat="density", common_norm=False, alpha=0.25)

plt.title("Figure 3 – Toxicity Distribution Across Platforms (Perspective API)", fontsize=14, pad=15)
plt.xlabel("Toxicity Score (0–1)", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.legend(title="Platform", labels=["Reddit", "/pol/ (4chan)"])
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# ------------------------------------------------------------------
# Save figure
# ------------------------------------------------------------------
output_path = "figure3_toxicity_distribution.png"
plt.savefig(output_path, dpi=300)
plt.close()
logging.info(f"Saved Figure 3 as {output_path}")