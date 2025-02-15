import json

import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from speedrun.celery import celery_app

logger = get_task_logger(__name__)


@shared_task
def execute_scheduled_trigger(trigger_id: int, trigger_time: str):
    """
    Executes a scheduled trigger.
    """
    return f"Executing Scheduled Trigger {trigger_id} at {trigger_time}"
    # Log execution in the database (to be implemented)


@celery_app.task
def execute_api_trigger(trigger_id: int, api_url: str, payload: dict):
    """
    Executes an API trigger by making a request.
    """
    logger.info(
        f"Executing API Trigger {trigger_id} with payload {json.dumps(payload)}",
    )
    try:
        response = requests.post(api_url, json=payload)
        logger.info(f"Response: {response.status_code}, {response.text}")
    except Exception as e:
        logger.info(f"API Call Failed: {e}")
