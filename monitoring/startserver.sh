#! /bin/bash
source /env/bin/activate

uvicorn monitoring.asgi:app --reload --debug --host 0.0.0.0 &

celery -A monitoring worker -l info -P celery_pool_asyncio:TaskPool

