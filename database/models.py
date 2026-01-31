
from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        tags TEXT,
        job_url TEXT UNIQUE,
        source TEXT,
        date_posted TEXT,
        date_scraped TEXT
    )
    """)

    conn.commit()
    conn.close()
