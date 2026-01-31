
from datetime import datetime, timezone
import sqlite3
from pathlib import Path

DB_PATH = Path("database/roverjobpulse.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def insert_jobs(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    now_utc = datetime.now(timezone.utc).isoformat()

    for job in jobs:
        try:
            cursor.execute("""
            INSERT INTO jobs (
                title, company, location, tags,
                job_url, source, date_posted, date_scraped
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job["title"],
                job["company"],
                job.get("location"),
                job.get("tags"),
                job["job_url"],
                job["source"],
                job.get("date_posted"),
                now_utc
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            # Duplicate job_url
            pass

    conn.commit()
    conn.close()
    return inserted
