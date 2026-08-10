import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

script_dir = Path(__file__).resolve().parent.parent
ENV_PATH = script_dir / "Echodatabse.env"

print(ENV_PATH)
print(ENV_PATH.exists())

load_dotenv(ENV_PATH)

try: 
    print(os.environ.get("DB_HOST"), os.environ.get("DB_PORT"), os.environ.get("DB_NAME"), os.environ.get("DB_USER"))
    with psycopg.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        password=os.environ.get("DB_PASS"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER")
    ) as connection:
       with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

            result = cursor.fetchone()
            print(f"Server response: {result}")
except psycopg.OperationalError as e:
    print(f"Database connection failed: {e}")