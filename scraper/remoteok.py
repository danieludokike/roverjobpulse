
import requests
from datetime import datetime, timezone
from scraper.base import BaseScraper


class RemoteOKScraper(BaseScraper):
    URL = "https://remoteok.com/api"

    def __init__(self):
        super().__init__("RemoteOK")

    def fetch_jobs(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.URL, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        jobs = []

        # First item is metadata
        for item in data[1:]:
            tags = item.get("tags", [])
            if "python" not in [t.lower() for t in tags]:
                continue

            # Handle job post date safely
            date_posted = None

            if item.get("date"):
                # ISO format
                date_posted = item["date"]
            elif item.get("epoch"):
                # Unix timestamp
                date_posted = datetime.fromtimestamp(
                    item["epoch"], tz=timezone.utc
                ).isoformat()

            jobs.append({
                "title": item.get("position"),
                "company": item.get("company"),
                "location": item.get("location"),
                "tags": ", ".join(tags),
                "job_url": item.get("url"),
                "source": self.source_name,
                "date_posted": date_posted
            })

        return jobs
