
from scraper.remoteok import RemoteOKScraper
from database.models import create_tables
from database.db import insert_jobs

def main():
    print("Starting RoverJobPulse scrape...")

    create_tables()

    scraper = RemoteOKScraper()
    jobs = scraper.fetch_jobs()

    inserted = insert_jobs(jobs)

    print(f"Fetched {len(jobs)} jobs")
    print(f"Inserted {inserted} new jobs into database")

if __name__ == "__main__":
    main()
