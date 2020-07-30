import aiopg
import aiopg.sa

import user_auth.app.settings as settings


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
