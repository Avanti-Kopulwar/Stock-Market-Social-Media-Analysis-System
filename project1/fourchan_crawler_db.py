import requests
import psycopg2
from psycopg2 import OperationalError
import time
import re
import json
from datetime import datetime
import logging
import sys

# ---- Logging Setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/fourchan.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# ---- CONFIG ----
BOARDS = ["biz", "pol", "g"]
FETCH_LIMIT = 5
SLEEP_TIME = 300  # seconds (5 min)

# ---- Load config ----
with open("config.json") as f:
    cfg = json.load(f)
db_cfg = cfg["database"]

# ---- Fix DB host if running on VM ----
if db_cfg["host"] == "postgres-db":
    db_cfg["host"] = "localhost"

# ---- DB connection with retry ----
def connect_db(retries=10, delay=10):
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**db_cfg)
            logging.info(f" Connected to PostgreSQL (attempt {attempt})")
            return conn
        except OperationalError as e:
            logging.warning(f"DB connection failed (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    logging.error(" Could not connect to database after retries.")
    sys.exit(1)

conn = connect_db()
cursor = conn.cursor()

# ---- Utility: clean text ----
def clean_comment(text):
    if not text:
        return ""
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"&gt;.*", "", text)
    text = re.sub(r"&.*?;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---- Insert post into DB ----
def save_post(post, board, thread_id):
    try:
        comment = clean_comment(post.get("com", ""))
        ts = datetime.utcfromtimestamp(post.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO chan_posts (post_id, board, thread_id, name, comment, created_utc)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_id) DO NOTHING;
        """, (
            post.get("no"),
            board,
            thread_id,
            post.get("name", "Anonymous"),
            comment,
            ts
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"DB ERROR Failed to insert post {post.get('no')}: {e}")

# ---- Fetch one thread ----
def fetch_thread(board, thread_id):
    url = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            logging.warning(f"[{board}] Thread {thread_id} HTTP {res.status_code}")
            return 0

        thread_data = res.json()
        posts = thread_data.get("posts", [])
        for post in posts:
            save_post(post, board, thread_id)

        return len(posts)
    except Exception as e:
        logging.error(f"[{board}] Thread fetch failed ({thread_id}): {e}")
        return 0

# ---- Fetch board ----
def fetch_board(board):
    url = f"https://a.4cdn.org/{board}/catalog.json"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        catalog = res.json()

        total_posts = 0
        for page in catalog:
            for thread in page.get("threads", [])[:FETCH_LIMIT]:
                total_posts += fetch_thread(board, thread["no"])

        logging.info(f"[{board}]  {total_posts} posts saved.")
    except Exception as e:
        logging.error(f"[{board}]  Board fetch error: {e}")

# ---- Main loop ----
def crawl_4chan():
    while True:
        start = datetime.now()
        for board in BOARDS:
            fetch_board(board)
            time.sleep(2)
        logging.info(f"Round finished at {start}, sleeping {SLEEP_TIME/60:.1f} minutes...\n")
        time.sleep(SLEEP_TIME)

# ---- ENTRY POINT ----
if __name__ == "__main__":
    logging.info(" Starting 4chan crawler...")
    try:
        crawl_4chan()
    except KeyboardInterrupt:
        logging.info("4chan crawler stopped manually.")
    except Exception as e:
        logging.error(f" Unexpected error in 4chan crawler: {e}")
