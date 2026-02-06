import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DB_CONFIG = {
    "dbname": "social_media",
    "user": "sjadhav",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

logging.info("Generating Figure 1 – Daily Post Counts: Reddit vs /pol/ (Sept–Dec)")

conn = psycopg2.connect(**DB_CONFIG)

query = """
WITH reddit_daily AS (
    SELECT 
        DATE(
            CASE 
                WHEN created_utc::text ~ '^[0-9]+$' THEN TO_TIMESTAMP(created_utc::text::double precision)
                ELSE created_utc
            END
        ) AS day,
        COUNT(*) AS reddit_posts
    FROM reddit_posts
    WHERE created_utc IS NOT NULL
    GROUP BY 1
),
pol_daily AS (
    SELECT DATE(created_utc) AS day, COUNT(*) AS pol_posts
    FROM chan_posts
    WHERE board = 'pol'
    GROUP BY 1
)
SELECT 
    d.day,
    COALESCE(r.reddit_posts, 0) AS reddit_posts,
    COALESCE(c.pol_posts, 0) AS pol_posts
FROM (
    SELECT GENERATE_SERIES(
        (SELECT LEAST(MIN(r.day), MIN(p.day)) FROM reddit_daily r, pol_daily p),
        (SELECT GREATEST(MAX(r.day), MAX(p.day)) FROM reddit_daily r, pol_daily p),
        INTERVAL '1 day'
    )::date AS day
) d
LEFT JOIN reddit_daily r ON d.day = r.day
LEFT JOIN pol_daily c ON d.day = c.day
WHERE d.day BETWEEN '2025-09-15' AND '2025-12-01'
ORDER BY d.day;
"""

df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    logging.warning("No data found.")
else:
    logging.info(f"Fetched {len(df)} days of data.")

    plt.figure(figsize=(10, 6))
    plt.plot(df["day"], df["reddit_posts"], label="Reddit", color="#FF4500", linewidth=2)
    plt.plot(df["day"], df["pol_posts"], label="/pol/ (4chan)", color="#2E8B57", linewidth=2)

    plt.title("Figure 1 – Daily Post Counts: Reddit vs /pol/ (Sept–Dec 2025)", fontsize=13)
    plt.xlabel("Date (Month–Day, 2025)", fontsize=11)
    plt.ylabel("Posts per Day", fontsize=11)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.gca().xaxis.set_major_formatter(DateFormatter("%m-%d"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_file = "figure1_daily_post_counts_final.png"
    plt.savefig(output_file, dpi=300)
    plt.show()
    logging.info(f"Plot saved successfully as {output_file}")