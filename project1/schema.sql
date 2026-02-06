
CREATE TABLE IF NOT EXISTS reddit_posts (
    post_id       TEXT PRIMARY KEY,
    subreddit     TEXT,
    title         TEXT,
    body          TEXT,
    author        TEXT,
    score         INTEGER,
    num_comments  INTEGER,
    created_utc   TIMESTAMP,
    retrieved_on  TIMESTAMP DEFAULT NOW(),
    url           TEXT
);

CREATE TABLE IF NOT EXISTS comments_for_reddits (
    comment_id    TEXT PRIMARY KEY,
    post_id       TEXT REFERENCES reddit_posts(post_id),
    subreddit     TEXT,
    author        TEXT,
    body          TEXT,
    score         INTEGER,
    created_utc   TIMESTAMP,
    retrieved_on  TIMESTAMP,
    comment_parent TEXT
);

-- ---------- 4chan Tables ----------
CREATE TABLE IF NOT EXISTS chan_posts (
    post_id       BIGINT PRIMARY KEY,
    thread_id     BIGINT,
    board         TEXT,
    name          TEXT,
    comment       TEXT,
    created_utc   TIMESTAMP,
    retrieved_on  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chan_posts_board_time
    ON chan_posts (board, created_utc DESC);

-- ---------- Aggregated Log Table ----------
CREATE TABLE IF NOT EXISTS grand_total_logs (
    id            SERIAL PRIMARY KEY,
    timestamp     TIMESTAMP,
    reddit_count  INTEGER,
    chan_count    INTEGER,
    total_count   INTEGER,
    timezone      TEXT
);
