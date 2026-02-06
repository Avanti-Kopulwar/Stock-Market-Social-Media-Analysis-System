import praw
import psycopg2
from psycopg2 import OperationalError
import json
import time
from datetime import datetime
import random
import logging
import sys

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/reddit.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# ---- Load Config ----
with open("config.json") as f:
    cfg = json.load(f)

db_cfg = cfg["database"]
reddit_cfg = cfg["reddit_credentials"]
subreddits = cfg["subreddits"]
fetch_limit = cfg.get("fetch_limit", 100)
sleep_time = cfg.get("sleep_time", 2)

# ---- Fix DB host for VM ----
if db_cfg["host"] == "postgres-db":
    db_cfg["host"] = "localhost"

# ---- Connect to PostgreSQL with retry ----
def connect_db(retries=10, delay=10):
    for i in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**db_cfg)
            logging.info(f" Connected to PostgreSQL (attempt {i})")
            return conn
        except OperationalError as e:
            logging.warning(f"DB connection failed (attempt {i}/{retries}): {e}")
            time.sleep(delay)
    sys.exit(" Could not connect to database after retries.")

conn = connect_db()
cursor = conn.cursor()

# ---- Reddit API Auth ----
reddit = praw.Reddit(
    client_id=reddit_cfg["client_id"],
    client_secret=reddit_cfg["client_secret"],
    user_agent=reddit_cfg["user_agent"]
)

# ---- Save Reddit post ----
def save_post(post, subreddit):
    try:
        cursor.execute("""
            INSERT INTO reddit_posts (post_id, subreddit, title, score, num_comments, created_utc)
            VALUES (%s, %s, %s, %s, %s, to_timestamp(%s))
            ON CONFLICT (post_id) DO NOTHING;
        """, (
            post.id,
            subreddit,
            post.title,
            post.score,
            post.num_comments,
            int(post.created_utc)
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"DB ERROR Failed to insert post {post.id}: {e}")

# ---- Fetch one subreddit ----
def fetch_subreddit(sub):
    try:
        posts = list(reddit.subreddit(sub).new(limit=fetch_limit))
        count = 0
        for post in posts:
            save_post(post, sub)
            count += 1
        logging.info(f"[{sub}]  {count} posts saved.")
        return count
    except Exception as e:
        logging.error(f"[{sub}]  Error fetching: {e}")
        return 0

# ---- Handle rate-limits or 429 errors ----
def safe_fetch(sub):
    """Retry subreddit fetch if Reddit API rate-limits or fails"""
    attempts = 0
    while attempts < 5:
        try:
            return fetch_subreddit(sub)
        except Exception as e:
            if "429" in str(e) or "RATELIMIT" in str(e).upper():
                wait = (attempts + 1) * 30
                logging.warning(f"⏳ Rate limit hit for {sub}, sleeping {wait}s...")
                time.sleep(wait)
                attempts += 1
            else:
                logging.error(f"[{sub}] Unexpected error: {e}")
                break
    return 0

# ---- Main crawler loop ----
def crawl_reddit():
    while True:
        start_time = datetime.now()
        shuffled_subs = random.sample(subreddits, len(subreddits))  # shuffle each round
        total_posts = 0

        for sub in shuffled_subs:
            total_posts += safe_fetch(sub)
            time.sleep(sleep_time)

        logging.info(f" Round finished at {start_time} | Total saved this round: {total_posts}")
        logging.info(f" Sleeping {(sleep_time * 5):.1f}s before next round...\n")
        time.sleep(sleep_time * 5)

# ---- Entry point ----
if __name__ == "__main__":
    logging.info("Starting Reddit crawler...")
    try:
        crawl_reddit()
    except KeyboardInterrupt:
        logging.info("Reddit crawler stopped manually.")
    except Exception as e:
        logging.error(f"Unexpected error in Reddit crawler: {e}")
