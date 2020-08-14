from aiohttp import web
from aiohttp_swagger import setup_swagger

import user_auth.app.jwt_pair as jwt_pair
from user_auth.app.db import close_pg, init_pg
from user_auth.app.routes import setup_routes


async def index(request):
    return web.Response(text="Welcome home!")


async def user_app():
    jwt_middleware = jwt_pair.middleware(whitelist=[r"api/doc*"])

    app = web.Application(middlewares=[jwt_middleware])
    setup_routes(app)
    setup_swagger(app)

    # db init/close
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    # jwt init/close (redis mostly)
    app.on_startup.append(jwt_pair.init_storage)
    app.on_cleanup.append(jwt_pair.close_storage)

    return app
