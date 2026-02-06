# Project 1 Report

## Repository Contents
- `project_1_report_sj_ak.pdf` – Final report in ACM SIGCONF format.  
- `reddit_crawler_db.py` – Reddit crawler for stock-related subreddits.  
- `fourchan_crawler_db.py` – 4chan crawler for /biz/, /pol/, and /g/ boards.  
- `grand_total.py` – Tracks total post counts across both platforms.  
- `config.json` – Runtime configuration for dynamic subreddit and board updates.  

---

## Run Commands
```bash
source venv/bin/activate
docker compose up -d
python3 reddit_crawler_db.py
python3 fourchan_crawler_db.py
python3 grand_total.py
