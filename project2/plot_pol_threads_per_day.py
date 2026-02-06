#!/usr/bin/env python3
"""
Figure 7 – /pol/ Threads per Day (Nov 1–14, 2025)
Counts how many unique threads were first created per day on 4chan's /pol/ board.
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import matplotlib.dates as mdates
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")
logging.info("Generating Figure 7 – /pol/ Threads per Day (Nov 1–14, 2025)")

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"
)

query = """
WITH thread_first_post AS (
    SELECT thread_id, MIN(created_utc) AS thread_start
    FROM chan_posts
    WHERE board = 'pol'
    GROUP BY thread_id
)
SELECT DATE(thread_start) AS day, COUNT(*) AS thread_count
FROM thread_first_post
WHERE thread_start::date BETWEEN '2025-11-01' AND '2025-11-14'
GROUP BY DATE(thread_start)
ORDER BY day;
"""

df = pd.read_sql_query(query, conn)
conn.close()
logging.info(f"Loaded {len(df)} rows for daily thread counts")

# Ensure 'day' is recognized as a date
df["day"] = pd.to_datetime(df["day"])

# Plot
plt.figure(figsize=(9,6))
plt.bar(df["day"], df["thread_count"], color="#ff7f0e", width=0.8)

plt.title("Figure 7 – /pol/ Threads per Day (Nov 1–14, 2025)", pad=15)
plt.xlabel("Date (November 2025)")
plt.ylabel("Threads Created")

# Format X-axis as dates (no time)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.xticks(rotation=45, ha="right")

plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

plt.savefig("figure7_pol_threads_per_day.png", dpi=300)
plt.close()
logging.info("Saved figure7_pol_threads_per_day.png")