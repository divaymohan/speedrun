from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from speedrun.db.models.event_logs import EventLog


class EventLogsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event: EventLog) -> EventLog:
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_events(self) -> Sequence[EventLog]:
        result = await self.db.execute(select(EventLog))
        return result.scalars().all()

    async def get_events_by_trigger_id(self, trigger_id: int) -> Sequence[EventLog]:
        result = await self.db.execute(select(EventLog).where(EventLog.trigger_id == trigger_id))
        event_logs = result.scalars().all()
        return event_logs



