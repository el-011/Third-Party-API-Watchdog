from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DashboardEndpointStatus(BaseModel):
    id: int
    url: str
    last_status: Optional[str]
    last_checked: Optional[datetime]
    uptime_percentage: Optional[float]

    model_config = ConfigDict(from_attributes=True)
