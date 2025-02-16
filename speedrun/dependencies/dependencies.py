from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from speedrun.db.dependencies import get_db_session
from speedrun.repo.event_logs import EventLogsRepo
from speedrun.repo.trigger import TriggerRepo
from speedrun.services.event_logs import EventLogService
from speedrun.services.trigger import TriggerService


def get_trigger_repo(db: AsyncSession = Depends(get_db_session)) -> TriggerRepo:
    return TriggerRepo(db=db)


def get_event_log_repo(db: AsyncSession = Depends(get_db_session)) -> EventLogsRepo:
    return EventLogsRepo(db=db)


def get_trigger_service(repo=Depends(get_trigger_repo)):
    return TriggerService(repo=repo)


def get_event_log_service(repo=Depends(get_event_log_repo)):
    return EventLogService(repo=repo)
