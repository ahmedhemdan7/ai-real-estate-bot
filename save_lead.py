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

def save_lead(name, phone, budget, location, property_type, bedrooms):

    conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="An800900"
)

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leads
        (name, phone, budget, location, property_type, bedrooms)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        name,
        phone,
        budget,
        location,
        property_type,
        bedrooms
    ))

    conn.commit()

    cur.close()
    conn.close()