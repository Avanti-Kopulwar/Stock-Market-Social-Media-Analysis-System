#!/usr/bin/env python3
"""
Figure 6B – Top Terms from /pol/ Posts
Extracts most frequent non-stopwords from /pol/ posts (Sept–Dec 2025).
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from collections import Counter
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")
logging.info("Generating Figure 6B – Top /pol/ Terms by Frequency")

conn = psycopg2.connect(
    host="localhost",
    dbname="social_media",
    user="sjadhav",
    password="1234"
)

query = """
SELECT comment
FROM chan_posts
WHERE board = 'pol' AND created_utc >= '2025-09-01';
"""
df = pd.read_sql_query(query, conn)
conn.close()
logging.info(f"Fetched {len(df)} /pol/ posts")

text = " ".join(df["comment"].dropna().astype(str)).lower()
tokens = re.findall(r"\b[a-z]{3,}\b", text)

stopwords = set("""
the of to and a in for that is on it you this with as are be was by an at
from have or not we they but if their them then there were what your his her
""".split())

filtered = [w for w in tokens if w not in stopwords]
counts = Counter(filtered).most_common(15)
terms, freqs = zip(*counts)

plt.figure(figsize=(9,6))
plt.barh(terms[::-1], freqs[::-1], color="steelblue")
plt.title("Figure 6B – Top Terms in /pol/ Posts (Sept–Dec 2025)", pad=15)
plt.xlabel("Frequency")
plt.ylabel("Term")
plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()

plt.savefig("figure6b_top_pol_terms.png", dpi=300)
plt.close()
logging.info("Saved figure6b_top_pol_terms.png")