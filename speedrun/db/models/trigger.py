from sqlalchemy import JSON, Column, DateTime, Integer, Interval, String, func
from sqlalchemy.orm import relationship

from speedrun.db.base import Base


class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trigger_type = Column(String, nullable=False)  # 'scheduled' or 'api'

    # For scheduled triggers
    schedule_time = Column(DateTime, nullable=True)  # One-time execution
    schedule_interval = Column(Interval, nullable=True)  # Recurring interval

    # For API triggers
    api_payload = Column(JSON, nullable=True)  # Store API payload

    created_at = Column(DateTime, server_default=func.now())

    # Relationship with Event Logs
    event_logs = relationship(
        "EventLog",
        back_populates="trigger",
        cascade="all, delete",
    )
