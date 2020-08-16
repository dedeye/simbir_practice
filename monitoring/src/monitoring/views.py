from fastapi import APIRouter
from pydantic import BaseModel

from .models import Event

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
    return await Event.get_events(skip, limit)


def init_app(app):
    app.include_router(router, prefix="/api/v1")
