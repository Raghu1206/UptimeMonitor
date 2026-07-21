import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import crud

scheduler = BackgroundScheduler()


def check_url(db: Session, url_obj):
    """
    Performs a single health check for one URL
    and stores the result in the database.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url_obj.url,
            headers=headers,
            timeout=10,
            allow_redirects=True,
        )

        response_time = int(response.elapsed.total_seconds() * 1000)
        status_code = response.status_code

        is_up = status_code < 500

        print(
            f"[OK] {url_obj.url} | "
            f"HTTP {status_code} | "
            f"{response_time} ms"
        )

    except requests.RequestException as e:
        print(f"[ERROR] {url_obj.url} | {e}")

        response_time = None
        status_code = None
        is_up = False

    crud.create_health_check(
        db,
        url_obj.id,
        status_code,
        response_time,
        is_up,
    )


def ping_urls():
    db = SessionLocal()

    try:
        urls = crud.get_urls(db)

        print(f"\nChecking {len(urls)} monitored URLs...\n")

        for url_obj in urls:
            check_url(db, url_obj)

    finally:
        db.close()


def start_scheduler():
    ping_urls()

    scheduler.add_job(
        ping_urls,
        "interval",
        minutes=1,
        id="uptime-monitor",
        replace_existing=True,
    )

    scheduler.start()

    print("Uptime scheduler started.")