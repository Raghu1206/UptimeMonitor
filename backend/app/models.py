from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class MonitoredURL(Base):
    __tablename__ = "monitored_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    checks = relationship("HealthCheck", back_populates="url", cascade="all, delete-orphan")

class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("monitored_urls.id"), nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Integer, nullable=True)
    is_up = Column(Boolean, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)

    url = relationship("MonitoredURL", back_populates="checks")