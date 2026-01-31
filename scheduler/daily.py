
import schedule
import time
from datetime import datetime, timezone
from main import main


def run_daily_job():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{now}] Running RoverJobPulse scheduled job...")
    main()
    print(f"[{now}] Job completed.\n")


def start_scheduler():
    # Run once per day at 08:00 UTC
    schedule.every().day.at("08:00").do(run_daily_job)

    print("RoverJobPulse scheduler started.")
    print("Waiting for next scheduled run...\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()
