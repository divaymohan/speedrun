from fastapi.routing import APIRouter

from speedrun.web.api import monitoring, triggers

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(triggers.router)
