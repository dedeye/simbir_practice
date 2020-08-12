from fastapi import APIRouter
from pydantic import BaseModel

from .models import Event
from .tasks import store_event

router = APIRouter()


class EventModel(BaseModel):
    service: str
    url: str
    status_code: int
    request_timestamp: float
    response_time: float


@router.get("/event/{id}/")
async def get_event(id: int):
    evt = await Event.get_or_404(id)
    return evt.to_dict()


@router.get("/event/")
async def events(skip: int = 0, limit: int = 10):
    events = await Event.get_events(skip, limit)
    return [event.to_dict() for event in events]


@router.post("/event/")
async def add_event(event: EventModel):

    store_event.delay(**event.dict())

    return {"result": "ok"}


def init_app(app):
    app.include_router(router, prefix="/api/v1")
