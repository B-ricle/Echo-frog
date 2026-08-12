import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

script_dir = Path(__file__).resolve().parent.parent
ENV_PATH = script_dir / "Echodatabse.env"

load_dotenv(ENV_PATH)

def get_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        password=os.environ.get("DB_PASS"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER")
    )
