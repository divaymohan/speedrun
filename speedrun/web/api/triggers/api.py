from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from speedrun.db.dependencies import get_db_session
from speedrun.db.models.trigger import Trigger
from speedrun.tasks import execute_scheduled_trigger
from speedrun.web.api.triggers.schema import (
    TriggerCreate,
    TriggerResponse,
    TriggerType,
    TriggerUpdate,
)

router = APIRouter()


@router.post(
    path="/triggers",
    response_model=TriggerCreate,
    description="Api will help to create an event",
)
async def create_trigger(
    trigger_data: TriggerCreate,
    db: AsyncSession = Depends(get_db_session),
):
    # Validate scheduled triggers
    if trigger_data.trigger_type == TriggerType.SCHEDULED:
        if not trigger_data.schedule_time and not trigger_data.schedule_interval:
            raise HTTPException(
                status_code=400,
                detail="Scheduled trigger must have either a "
                "schedule_time or schedule_interval",
            )

    # Validate API triggers
    if trigger_data.trigger_type == TriggerType.API:
        if not trigger_data.api_payload:
            raise HTTPException(
                status_code=400,
                detail="API trigger must have a payload",
            )

    schedule_time = trigger_data.schedule_time
    if schedule_time and schedule_time.tzinfo is not None:
        schedule_time = schedule_time.astimezone(tz=None).replace(tzinfo=None)

    # Create trigger object
    new_trigger = Trigger(
        name=trigger_data.name,
        trigger_type=trigger_data.trigger_type,
        schedule_time=schedule_time,
        schedule_interval=timedelta(
            minutes=trigger_data.schedule_interval,
        )
        if trigger_data.schedule_interval
        else None,
        api_payload=trigger_data.api_payload,
    )

    db.add(new_trigger)
    await db.commit()
    await db.refresh(new_trigger)

    return TriggerResponse(
        id=new_trigger.id,
        name=new_trigger.name,
        trigger_type=new_trigger.trigger_type,
        schedule_time=new_trigger.schedule_time,
        schedule_interval=trigger_data.schedule_interval,
        api_payload=new_trigger.api_payload,
        created_at=new_trigger.created_at,
    )


@router.get("/triggers/", response_model=List[TriggerResponse])
async def get_all_triggers(db: AsyncSession = Depends(get_db_session)):
    """
    Retrieve all triggers.
    """
    async with db as session:
        result = await session.execute(select(Trigger))
        triggers = result.scalars().all()
        trigger_list = [
            TriggerResponse(
                id=new_trigger.id,
                name=new_trigger.name,
                trigger_type=new_trigger.trigger_type,
                schedule_time=new_trigger.schedule_time,
                schedule_interval=new_trigger.schedule_interval,
                api_payload=new_trigger.api_payload,
                created_at=new_trigger.created_at,
            )
            for new_trigger in triggers
        ]
        return trigger_list


@router.get("/triggers/{trigger_id}", response_model=TriggerResponse)
async def get_trigger_by_id(
    trigger_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Retrieve a single trigger by ID.
    """
    async with db as session:
        result = await session.execute(select(Trigger).where(Trigger.id == trigger_id))
        trigger = result.scalars().first()

        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")

        return trigger


@router.get("/triggers/{trigger_id}/start", response_model=str)
async def get_trigger_by_id(
    trigger_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Retrieve a single trigger by ID.
    """
    async with db as session:
        result = await session.execute(select(Trigger).where(Trigger.id == trigger_id))
        trigger = result.scalars().first()

        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")

        if trigger.trigger_type == "scheduled":
            # schedule_time = datetime.fromisoformat(str(trigger.schedule_time))
            execute_scheduled_trigger.apply_async(
                args=[trigger.id, trigger.schedule_time],
                countdown=2,
                repeat=True,
            )

        return "Trigger Triggered..!!"


@router.put(
    path="/triggers/{trigger_id}",
    response_model=TriggerResponse,
)
async def update_trigger(
    trigger_id: int,
    trigger_update: TriggerUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a trigger by ID.
    """
    async with db as session:
        result = await session.execute(select(Trigger).where(Trigger.id == trigger_id))
        trigger = result.scalars().first()

        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")

        # Update fields
        if trigger_update.name:
            trigger.name = trigger_update.name
        if trigger_update.schedule_time:
            trigger.schedule_time = trigger_update.schedule_time.replace(tzinfo=None)
        if trigger_update.schedule_interval:
            trigger.schedule_interval = trigger_update.schedule_interval
        if trigger_update.api_payload:
            trigger.api_payload = trigger_update.api_payload

        await session.commit()
        await session.refresh(trigger)
        return trigger


@router.delete(
    path="/triggers/{trigger_id}",
    status_code=204,
)
async def delete_trigger(trigger_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Delete a trigger by ID.
    """
    async with db as session:
        result = await session.execute(select(Trigger).where(Trigger.id == trigger_id))
        trigger = result.scalars().first()

        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")

        await session.delete(trigger)
        await session.commit()
        return {"message": "Trigger deleted successfully"}
