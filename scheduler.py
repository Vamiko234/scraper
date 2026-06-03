"""
Keeps running and fires the report daily at the configured UTC time.
Usage: python scheduler.py
"""
import schedule
import time
from datetime import datetime
from config import REPORT_HOUR_UTC, REPORT_MINUTE_UTC
from runner import run


def job():
    try:
        run()
    except Exception as e:
        print(f"[Scheduler] Report failed: {e}")


run_time = f"{REPORT_HOUR_UTC:02d}:{REPORT_MINUTE_UTC:02d}"
schedule.every().day.at(run_time, "UTC").do(job)

print(f"Scheduler started. Daily report at {run_time} UTC.")
print("Press Ctrl+C to stop.\n")

while True:
    schedule.run_pending()
    time.sleep(30)
