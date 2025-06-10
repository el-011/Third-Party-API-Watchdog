from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime

class EndpointBase(BaseModel):
    url: str
    expected_status_code: int
    expected_response_schema: Optional[Dict[str, Any]] = None

class EndpointCreate(EndpointBase):
    pass

class EndpointOut(EndpointBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
