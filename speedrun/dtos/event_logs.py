from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TriggerType(str, Enum):
    API = "api"
    SCHEDULED = "scheduled"


class EventLogCreate(BaseModel):
    trigger_id: int
    event_type: TriggerType
    payload: dict
    response: str


class EventLogResponse(BaseModel):
    id: int
    trigger_id: int
    event_time: datetime
    event_type: str
    payload: Optional[dict] = Field(default=None, description="Payload of api")
    archived: bool
    response: str
