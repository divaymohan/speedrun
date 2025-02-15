from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from speedrun.db.dependencies import get_db_session
from speedrun.repo.trigger import TriggerRepo
from speedrun.services.trigger import TriggerService


def get_trigger_repo(db: AsyncSession = Depends(get_db_session)) -> TriggerRepo:
    return TriggerRepo(db=db)


def get_trigger_service(repo=Depends(get_trigger_repo)):
    return TriggerService(repo=repo)
