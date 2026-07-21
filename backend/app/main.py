from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from . import models, schemas, crud, scheduler

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Uptime Monitor API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    scheduler.start_scheduler()


@app.post("/urls", response_model=schemas.URLResponse)
def add_url(
    url_in: schemas.URLCreate,
    db: Session = Depends(get_db)
):
    db_url = crud.get_url_by_address(db, url_in.url)

    if db_url:
        raise HTTPException(
            status_code=400,
            detail="URL already being monitored"
        )

    created = crud.create_url(db, url_in)

    scheduler.check_url(db, created)

    return created


@app.get("/urls", response_model=List[schemas.URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    return crud.get_urls(db)


@app.get("/status", response_model=List[schemas.StatusResponse])
def get_latest_status(db: Session = Depends(get_db)):
    urls = crud.get_urls(db)
    result = []

    for url_obj in urls:

        latest_check = (
            db.query(models.HealthCheck)
            .filter(models.HealthCheck.url_id == url_obj.id)
            .order_by(models.HealthCheck.checked_at.desc())
            .first()
        )

        if latest_check is None:

            status = "PENDING"
            response_time = None
            status_code = None

        else:

            status_code = latest_check.status_code
            response_time = latest_check.response_time

            if status_code is None:

                status = "DOWN"

            elif status_code >= 500:

                status = "DOWN"

            elif status_code >= 400:

                status = "RESTRICTED"

            else:

                status = "UP"

        result.append(
            {
                "url": url_obj.url,
                "status": status,
                "status_code": status_code,
                "response_time": response_time,
            }
        )

    return result