import asyncio

from celery import Celery
from celery.signals import celeryd_init
from monitoring import config
from monitoring.models import db

app = Celery(
    "monitoring", broker="amqp://guest:guest@rabbit/", include=["monitoring.tasks"]
)


@celeryd_init.connect
def configure_db(**kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db.set_bind(config.DB_DSN))
