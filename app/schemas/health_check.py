from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class HealthCheckOut(BaseModel):
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    check_time: datetime
    status: str
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
