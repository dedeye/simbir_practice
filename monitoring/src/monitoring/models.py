from gino.ext.starlette import Gino

from . import config

db = Gino(
    dsn=config.DB_DSN,
    pool_min_size=config.DB_POOL_MIN_SIZE,
    pool_max_size=config.DB_POOL_MAX_SIZE,
    echo=config.DB_ECHO,
    ssl=config.DB_SSL,
    use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=config.DB_RETRY_LIMIT,
    retry_interval=config.DB_RETRY_INTERVAL,
)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.BigInteger(), primary_key=True)
    service = db.Column(db.String(60), nullable=False)
    url = db.Column(db.String, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    request_timestamp = db.Column(db.Float)
    response_time = db.Column(db.Float)

    @classmethod
    async def get_events(self, skip, limit):
        async with db.transaction():
            cursor = await Event.query.gino.iterate()
            if skip > 0:
                await cursor.forward(skip)
            events = await cursor.many(limit)
        return events
