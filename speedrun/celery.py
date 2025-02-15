import os

from celery import Celery

celery_app = Celery(__name__)


celery_app.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    redbeat_redis_url=os.getenv("RED_BEAT_REDIS_URL", "redis://redis:6379/0"),
    beat_scheduler="redbeat.RedBeatScheduler",
    timezone="Asia/Kolkata",  # Setting timezone to IST
    enable_utc=False,  # Disable UTC to use the specified timezone
)
