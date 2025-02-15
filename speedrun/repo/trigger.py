from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from speedrun.db.models.trigger import Trigger


class TriggerRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trigger(self, trigger: Trigger) -> Trigger:
        self.db.add(trigger)
        await self.db.commit()
        await self.db.refresh(trigger)
        return trigger

    async def get_triggers(self) -> Sequence[Trigger]:
        result = await self.db.execute(select(Trigger))
        return result.scalars().all()

    async def get_trigger(self, trigger_id: int) -> Trigger:
        result = await self.db.execute(select(Trigger).where(Trigger.id == trigger_id))
        trigger = result.scalar()
        return trigger

    async def delete_trigger(self, trigger_id: int):
        trigger = await self.get_trigger(trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        await self.db.delete(trigger)
        await self.db.commit()

    async def update_trigger(self, trigger_id: int, trigger_data: dict) -> Trigger:
        trigger = await self.get_trigger(trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        for key, value in trigger_data.items():
            setattr(trigger, key, value)
        await self.db.commit()
        await self.db.refresh(trigger)
        return trigger
