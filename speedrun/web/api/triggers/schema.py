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

    # class Config:
    #     orm_mode = True


class TriggerResponse(BaseModel):
    id: int
    name: str
    trigger_type: TriggerType
    schedule_time: Optional[datetime] = None
    schedule_interval: Optional[int] = None
    api_payload: Optional[dict] = None
    created_at: datetime

    # class Config:
    #     orm_mode = True


class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    schedule_time: Optional[datetime] = None
    schedule_interval: Optional[int] = None
    api_payload: Optional[dict] = None

    # class Config:
    #     orm_mode = True
