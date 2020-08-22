from monitoring.models import Event

from .celeryapp import app


@app.task
async def store_event(**params):
    await Event.create(**params)
