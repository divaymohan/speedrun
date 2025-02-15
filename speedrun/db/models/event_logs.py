from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from speedrun.db.base import Base


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer, ForeignKey("triggers.id", ondelete="CASCADE"))
    event_time = Column(DateTime, server_default=func.now())  # When the event was fired
    event_type = Column(String, nullable=False)  # 'scheduled', 'api', or 'manual_test'
    payload = Column(JSON, nullable=True)  # Store API payload if applicable
    archived = Column(Boolean, default=False)  # If the log has been archived

    # Relationship
    trigger = relationship("Trigger", back_populates="event_logs")
