import uuid

from gino.ext.starlette import Gino

from sqlalchemy.dialects.postgresql import UUID

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


class Template(db.Model):
    __tablename__ = "templates"
    id = db.Column(
        UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False,
    )
    name = db.Column(db.String(80), nullable=False, unique=True)
    subject = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    @classmethod
    async def get_by_name(self, name):
        return await Template.query.where(Template.name == name).gino.first()
