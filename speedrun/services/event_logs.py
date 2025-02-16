from typing import List, Sequence, cast

from speedrun.db.models.event_logs import EventLog as EventLogEntity
from speedrun.dtos.event_logs import EventLogCreate, EventLogResponse
from speedrun.repo.event_logs import EventLogsRepo


class EventLogService:
    def __init__(self, repo: EventLogsRepo):
        self.repo = repo

    async def create_event(self, event_data: EventLogCreate) -> EventLogEntity:
        event_log_entity: EventLogEntity = EventLogEntity(
            trigger_id=event_data.trigger_id,
            event_type=event_data.event_type,
            payload=event_data.payload,
            response=event_data.response,
        )

        event: EventLogEntity = await self.repo.create_event(event=event_log_entity)
        return event

    async def get_events(self) -> List[EventLogResponse]:
        event_log_list: Sequence[EventLogEntity] = await self.repo.get_events()
        event_log_response_list = []
        for event in event_log_list:
            event_log: EventLogEntity = cast(EventLogEntity, event)
            event_log_response_list.append(
                EventLogResponse(
                    id=event_log.id,
                    trigger_id=event_log.trigger_id,
                    event_time=event_log.event_time,
                    event_type=event_log.event_type,
                    payload=event_log.payload,
                    archived=event_log.archived,
                    response=event_log.response,
                ),
            )
        return event_log_response_list

    async def get_events_by_trigger_id(self, trigger_id: int) -> List[EventLogResponse]:
        event_log_list: Sequence[
            EventLogEntity
        ] = await self.repo.get_events_by_trigger_id(
            trigger_id=trigger_id,
        )
        event_log_response_list = []
        for event in event_log_list:
            event_log: EventLogEntity = cast(EventLogEntity, event)
            event_log_response_list.append(
                EventLogResponse(
                    id=event_log.id,
                    trigger_id=event_log.trigger_id,
                    event_time=event_log.event_time,
                    event_type=event_log.event_type,
                    payload=event_log.payload,
                    archived=event_log.archived,
                    response=event_log.response,
                ),
            )
        return event_log_response_list
