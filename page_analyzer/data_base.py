import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def save_url(url):
    sql = ("INSERT INTO urls (name) VALUES (%s) RETURNING id;", (url,))
    with get_db_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            url_id = curs.fetchone()[0]
            conn.commit()
            return url_id