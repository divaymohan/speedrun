from typing import List

from fastapi import APIRouter, Depends

from speedrun.dependencies.dependencies import get_trigger_service
from speedrun.services.trigger import TriggerService
from speedrun.web.api.triggers.schema import (
    TriggerCreate,
    TriggerResponse,
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
    service: TriggerService = Depends(get_trigger_service),
):
    response: TriggerResponse = await service.create_trigger(trigger_data=trigger_data)
    return response


@router.get(
    path="/triggers",
    response_model=List[TriggerResponse],
)
async def get_all_triggers(
    service: TriggerService = Depends(get_trigger_service),
):
    """
    Retrieve all triggers.
    """
    return await service.get_triggers()


@router.get(
    path="/triggers/{trigger_id}",
    response_model=TriggerResponse,
)
async def get_trigger_by_id(
    trigger_id: int,
    service: TriggerService = Depends(get_trigger_service),
):
    response: TriggerResponse = await service.get_trigger(trigger_id=trigger_id)
    return response


@router.get("/triggers/{trigger_id}/start", response_model=str)
async def get_trigger_by_id(
    trigger_id: int,
    service: TriggerService = Depends(get_trigger_service),
):
    """
    Retrieve a single trigger by ID.
    """
    return await service.trigger_event(trigger_id=trigger_id)


@router.put(
    path="/triggers/{trigger_id}",
    response_model=TriggerResponse,
)
async def update_trigger(
    trigger_id: int,
    trigger_update: TriggerUpdate,
    service: TriggerService = Depends(get_trigger_service),
):
    """
    Update a trigger by ID.
    """
    return await service.update_trigger(
        trigger_id=trigger_id,
        trigger_update=trigger_update,
    )


@router.delete(
    path="/triggers/{trigger_id}",
    status_code=204,
)
async def delete_trigger(
    trigger_id: int,
    service: TriggerService = Depends(get_trigger_service),
):
    """
    Delete a trigger by ID.
    """
    await service.delete_trigger(trigger_id=trigger_id)
    return {"message": "Trigger deleted successfully"}
