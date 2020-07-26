import uuid

import aiopg
import aiopg.sa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import user_auth.app.settings as settings

metadata = sa.MetaData(schema="users")

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, index=True),
    sa.Column("username", sa.String(200), unique=True, nullable=False),
    sa.Column("password", sa.String(100), nullable=False),
    sa.Column("role", sa.String(20), nullable=False),
)


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=settings.DATABASE["NAME"],
        user=settings.DATABASE["USER"],
        password=settings.DATABASE["PASSWORD"],
        host=settings.DATABASE["HOST"],
        port=settings.DATABASE["PORT"],
    )
    app["db"] = engine


async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()


async def create_user(conn, username, passhash, role):
    stmt = users.insert().values(
        id=uuid.uuid4(), username=username, password=passhash, role=role,
    )
    await conn.execute(stmt)


async def get_user(conn, username):
    stmt = users.select().where(users.c.username == username)
    result = await conn.execute(stmt)
    return await result.fetchone()
