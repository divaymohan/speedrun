import json

import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from speedrun.db.internal_db import get_internal_db_session
from speedrun.db.models.event_logs import EventLog as EventLogEntity

logger = get_task_logger(__name__)


@shared_task
def execute_scheduled_trigger(
    trigger_id: int,
    trigger_time: str,
    payload: dict = None,
):
    """
    Executes a scheduled trigger.
    """
    message: str = f"Executing Scheduled Trigger {trigger_id} at {trigger_time}"
    import asyncio

    from speedrun.repo.event_logs import EventLogsRepo

    async def log_event():
        async with get_internal_db_session() as session:
            event_log_repo: EventLogsRepo = EventLogsRepo(db=session)

            event_log_entity: EventLogEntity = EventLogEntity(
                trigger_id=trigger_id,
                event_type="scheduled",
                payload=payload,
                response=message,
            )

            await event_log_repo.create_event(event=event_log_entity)

    asyncio.run(log_event())  # Convert async to sync

    return message


@shared_task
def execute_api_trigger(trigger_id: int, api_url: str, payload: dict = None):
    """
    Executes an API trigger by making a request.
    """
    logger.info(
        f"Executing API Trigger {trigger_id} with payload {json.dumps(payload)}",
    )
    try:
        response = requests.post(api_url, json=payload)
        _store_event(trigger_id, response.status_code, response.text, payload)

        logger.info(f"Response: {response.status_code}, {response.text}")
    except Exception as e:
        _store_event(trigger_id, 500, f"API Call Failed: {e}", payload)
        logger.info(f"API Call Failed: {e}")


def _store_event(trigger_id: int, status_code: int, text: str, payload: dict = None):
    import asyncio

    from speedrun.repo.event_logs import EventLogsRepo

    async def log_event():
        async with get_internal_db_session() as session:
            event_log_repo: EventLogsRepo = EventLogsRepo(db=session)

            event_log_entity: EventLogEntity = EventLogEntity(
                trigger_id=trigger_id,
                event_type="scheduled",
                payload=payload,
                response=f"Response: {status_code}, {text}",
            )

            await event_log_repo.create_event(event=event_log_entity)

    asyncio.run(log_event())  # Convert async to sync
