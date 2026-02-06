import psycopg2
import json
import os

def get_postgres_connection():
    # config.json is in the folder: /home/sjadhav/social_media/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    config_path = os.path.join(base_dir, "config.json")

    with open(config_path) as f:
        cfg = json.load(f)

    db = cfg["database"]  # correct key

    return psycopg2.connect(
        host=db["host"],
        user=db["user"],
        password=db["password"],
        database=db["database"],
        port=5432
    )
