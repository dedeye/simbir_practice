from aiohttp import web

from .routes import setup_routes


async def index(request):
    return web.Response(text="Welcome home!")


async def get_app():

    app = web.Application()
    setup_routes(app)
    app.router.add_route("GET", "", index)
    return app
