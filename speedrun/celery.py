from celery import Celery

celery_app = Celery(
    "event_trigger",
    broker="pyamqp://speedrun:speedrun@rabbitmq//",
    backend="rpc://"
)

celery_app.conf.task_routes = {
    "speedrun.tasks.execute_scheduled_trigger": {"queue": "scheduled_queue"},
    "speedrun.tasks.execute_api_trigger": {"queue": "api_queue"},
}
