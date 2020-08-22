from aiohttp import web
from aiohttp_swagger import setup_swagger

from .auth.mail_token import init_mail_token
from .mailing import mailing_init
from .monitoring import monitoring_middleware
from .routes import setup_routes


async def index(request):
    return web.Response(text="Welcome home!")


async def get_app():

    app = web.Application(middlewares=[monitoring_middleware])
    setup_routes(app)
    app.router.add_route("GET", "", index)
    setup_swagger(app, ui_version=3, swagger_from_file="openapi.yaml")
    mailing_init(app)
    init_mail_token(app)
    return app
