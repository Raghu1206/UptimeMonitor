from sqlalchemy.orm import Session
from . import models, schemas

def get_urls(db: Session):
    return db.query(models.MonitoredURL).all()

def get_url_by_address(db: Session, url: str):
    return db.query(models.MonitoredURL).filter(models.MonitoredURL.url == url).first()

def create_url(db: Session, url_schema: schemas.URLCreate):
    db_url = models.MonitoredURL(url=url_schema.url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def create_health_check(db: Session, url_id: int, status_code: int | None, response_time: int | None, is_up: bool):
    check = models.HealthCheck(
        url_id=url_id,
        status_code=status_code,
        response_time=response_time,
        is_up=is_up
    )
    db.add(check)
    db.commit()
    db.refresh(check)
    return check