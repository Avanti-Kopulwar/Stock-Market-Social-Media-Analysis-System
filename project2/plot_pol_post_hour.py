#!/usr/bin/env python3
"""
Figure 8 – /pol/ Posts per Hour (Nov 1–14, 2025)
Improved x-axis readability with hourly tick spacing adjustment.
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import matplotlib.dates as mdates
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")
logging.info("Generating Figure 8 – /pol/ Posts per Hour (Nov 1–14, 2025)")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"
)

query = """
SELECT DATE_TRUNC('hour', created_utc) AS hour, COUNT(*) AS post_count
FROM chan_posts
WHERE board = 'pol'
  AND created_utc BETWEEN '2025-11-01' AND '2025-11-14'
GROUP BY DATE_TRUNC('hour', created_utc)
ORDER BY hour;
"""

df = pd.read_sql_query(query, conn)
conn.close()
logging.info(f"Loaded {len(df)} hourly data points for /pol/ posts")

# Ensure datetime format
df["hour"] = pd.to_datetime(df["hour"])

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df["hour"], df["post_count"], color="#ff7f0e", linewidth=1.8)

plt.title("Figure 8 – /pol/ Posts per Hour (Nov 1–14, 2025)", pad=15)
plt.xlabel("Date & Hour (November 2025)")
plt.ylabel("Posts per Hour")

# Cleaner x-axis formatting
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))  # Show one tick every 3 hours
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
plt.xticks(rotation=45, ha="right", fontsize=9)

plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.savefig("figure8_pol_posts_per_hour.png", dpi=300)
plt.close()
logging.info("Saved figure8_pol_posts_per_hour.png (with cleaner x-axis)")