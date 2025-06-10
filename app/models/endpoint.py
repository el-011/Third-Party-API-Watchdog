from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from app.core.database import Base

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    expected_status_code = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expected_response_schema = Column(Text, nullable=True)

    checks = relationship("HealthCheck", back_populates="endpoint", cascade="all, delete-orphan")
