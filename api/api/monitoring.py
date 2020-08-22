from datetime import datetime

from aiohttp.web import middleware
from celery import Celery

from api.settings import config

app = Celery("monitoring", broker=config.get_monitor_rabbit_url())


def add_event(service, url, status_code, request_timestamp, response_time):
    app.send_task(config.monitor_task, kwargs=locals())


@middleware
async def monitoring_middleware(request, handler):
    service = "api"
    url = str(request.rel_url)
    request_timestamp = datetime.now().timestamp()
    resp = await handler(request)
    status_code = resp.status
    respone_time = datetime.now().timestamp() - request_timestamp

    add_event(service, url, status_code, request_timestamp, respone_time)

    return resp
