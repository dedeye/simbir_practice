from __future__ import absolute_import, unicode_literals

from monitoring.models import Event

from .celery import app


@app.task
async def store_event(**params):
    await Event.create(**params)
