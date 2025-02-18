from datetime import datetime, timedelta
from typing import List, Sequence, cast

from fastapi import HTTPException
from redbeat import RedBeatSchedulerEntry

from speedrun.celery import celery_app
from speedrun.db.models.trigger import Trigger as TriggerEntity
from speedrun.dtos.trigger import (
    TriggerCreate,
    TriggerResponse,
    TriggerType,
    TriggerUpdate,
)
from speedrun.repo.trigger import TriggerRepo
from speedrun.tasks import execute_api_trigger, execute_scheduled_trigger


class TriggerService:
    def __init__(self, repo: TriggerRepo):
        self.repo = repo

    async def create_trigger(self, trigger_data: TriggerCreate) -> TriggerResponse:
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
        trigger: TriggerEntity = TriggerEntity(
            name=trigger_data.name,
            trigger_type=trigger_data.trigger_type,
            schedule_time=schedule_time,
            schedule_interval=timedelta(
                seconds=trigger_data.schedule_interval,
            )
            if trigger_data.schedule_interval
            else None,
            api_payload=trigger_data.api_payload,
            api_url=trigger_data.api_url,
        )

        await self.repo.create_trigger(trigger=trigger)

        return TriggerResponse(
            id=trigger.id,
            name=trigger.name,
            trigger_type=trigger.trigger_type,
            schedule_time=trigger.schedule_time,
            schedule_interval=trigger_data.schedule_interval,
            api_payload=trigger.api_payload,
            created_at=trigger.created_at,
            api_url=trigger_data.api_url,
        )

    async def get_triggers(self) -> List[TriggerResponse]:
        trigger_list: Sequence[TriggerEntity] = await self.repo.get_triggers()
        trigger_response_list = []
        for trigger in trigger_list:
            trigger: TriggerEntity = cast(TriggerEntity, trigger)
            trigger_response_list.append(
                TriggerResponse(
                    id=trigger.id,
                    name=trigger.name,
                    trigger_type=trigger.trigger_type,
                    schedule_time=trigger.schedule_time,
                    schedule_interval=trigger.schedule_interval.total_seconds()
                    if trigger.schedule_interval
                    else 0,
                    api_payload=trigger.api_payload,
                    created_at=trigger.created_at,
                    api_url=trigger.api_url,
                ),
            )
        return trigger_response_list

    async def get_trigger(self, trigger_id: int) -> TriggerResponse:
        trigger: TriggerEntity = await self.repo.get_trigger(trigger_id=trigger_id)
        # TODO: if not trigger raise not found exception with code 404

        trigger_response: TriggerResponse = TriggerResponse(
            id=trigger.id,
            name=trigger.name,
            trigger_type=trigger.trigger_type,
            schedule_time=trigger.schedule_time,
            schedule_interval=trigger.schedule_interval.total_seconds(),
            api_payload=trigger.api_payload,
            created_at=trigger.created_at,
            api_url=trigger.api_url,
        )

        return trigger_response

    async def trigger_event(self, trigger_id: int) -> str:
        trigger: TriggerEntity = await self.repo.get_trigger(trigger_id=trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        if trigger.trigger_type == "scheduled":
            if not trigger.schedule_interval:
                schedule_time = datetime.fromisoformat(str(trigger.schedule_time))
                execute_scheduled_trigger.apply_async(
                    args=[trigger.id, trigger.schedule_time],
                    eta=schedule_time,
                )
            else:
                entry = RedBeatSchedulerEntry(
                    name=trigger.id,
                    task="speedrun.tasks.execute_scheduled_trigger",
                    schedule=trigger.schedule_interval,
                    args=(trigger.id, str(trigger.schedule_time)),
                    app=celery_app,
                )
                entry.save()
        else:
            schedule_time = datetime.fromisoformat(str(trigger.schedule_time))
            execute_api_trigger.apply_async(
                args=[trigger.id, trigger.api_url, trigger.api_payload],
                eta=schedule_time,
            )

        return "Event Triggered..!!"

    async def update_trigger(self, trigger_id: int, trigger_update: TriggerUpdate):
        trigger: TriggerEntity = await self.repo.update_trigger(
            trigger_id=trigger_id,
            trigger_data=trigger_update.model_dump(),
        )

        trigger_response: TriggerResponse = TriggerResponse(
            id=trigger.id,
            name=trigger.name,
            trigger_type=trigger.trigger_type,
            schedule_time=trigger.schedule_time,
            schedule_interval=trigger.schedule_interval.total_seconds(),
            api_payload=trigger.api_payload,
            created_at=trigger.created_at,
            api_url=trigger.api_url,
        )

        return trigger_response

    async def delete_trigger(self, trigger_id: int):
        try:
            entry = RedBeatSchedulerEntry(name=str(trigger_id), app=celery_app)
            entry.delete()
            await self.repo.delete_trigger(trigger_id=trigger_id)
            return "Scheduled event deleted successfully."
        except Exception as e:
            return f"Error deleting event: {str(e)}"
