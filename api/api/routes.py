from api.auth.views import routes as auth_routes


def setup_routes(app):
    app.router.add_routes(auth_routes)
