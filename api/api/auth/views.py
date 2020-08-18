from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/auth/get")
async def handle_get(request):
    return web.json_response(data={"result": "success"}, status=200)
