from api.auth.views import routes as auth_routes
from api.goods.views import routes as goods_routes


def setup_routes(app):
    app.router.add_routes(auth_routes)
    app.router.add_routes(goods_routes)
