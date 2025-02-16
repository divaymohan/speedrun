from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class TriggerType(str, Enum):
    API = "api"
    SCHEDULED = "scheduled"


class TriggerCreate(BaseModel):
    name: str = Field(..., example="My Trigger")
    trigger_type: TriggerType = Field(..., example="scheduled")  # "scheduled" or "api"

    # Scheduled trigger options
    schedule_time: Optional[datetime] = None  # One-time trigger
    schedule_interval: Optional[int] = None  # Recurring trigger (in minutes)

    # API trigger options
    api_payload: Optional[Dict[str, str]] = None  # JSON payload for API trigger
    api_url: Optional[str] = None

    # class Config:
    #     orm_mode = True


class TriggerResponse(BaseModel):
    id: int
    name: str
    trigger_type: TriggerType
    schedule_time: Optional[datetime] = None
    schedule_interval: Optional[int] = None
    api_payload: Optional[dict] = None
    api_url: Optional[str] = None
    created_at: datetime


class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    schedule_time: Optional[datetime] = None
    schedule_interval: Optional[int] = None
    api_payload: Optional[dict] = None
    api_url: Optional[str] = None
