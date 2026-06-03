# conversation.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="An800900"
    )


def get_messages(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT messages FROM conversations WHERE user_id=%s",
        (user_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return ""


def save_messages(user_id, messages):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO conversations (user_id, messages)
        VALUES (%s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET messages = EXCLUDED.messages
    """, (user_id, messages))

    conn.commit()

    cur.close()
    conn.close()