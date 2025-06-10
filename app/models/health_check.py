from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, Text, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id", ondelete="CASCADE"), nullable=False)
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    check_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    error_message = Column(Text, nullable=True)

    endpoint = relationship("Endpoint", back_populates="checks")
