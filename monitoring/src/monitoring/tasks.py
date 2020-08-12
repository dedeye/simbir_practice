from __future__ import absolute_import, unicode_literals

from monitoring.models import Event

from .celery import app


@app.task
async def store_event(**params):
    print(params)

    # await db.set_bind(config.DB_DSN)
    await Event.create(**params)
