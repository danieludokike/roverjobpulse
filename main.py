
from scraper.remoteok import RemoteOKScraper

def main():
    scraper = RemoteOKScraper()
    jobs = scraper.fetch_jobs()

    print(f"Fetched {len(jobs)} jobs")
    for job in jobs[:5]:
        print(job)

if __name__ == "__main__":
    main()
