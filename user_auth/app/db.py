import aiopg
import aiopg.sa

from user_auth.app.settings import config


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=config.db_name,
        user=config.db_user,
        password=config.db_pass,
        host=config.db_host,
        port=config.db_port,
    )
    app["db"] = engine


async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()
