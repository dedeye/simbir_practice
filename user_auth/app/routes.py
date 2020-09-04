import user_auth.app.views as views


def setup_routes(app):
    app.router.add_route("POST", "/api/v1/register/", views.register)
    app.router.add_route("POST", "/api/v1/login/", views.login)
    app.router.add_route("GET", "/api/v1/validate/", views.validate)
    app.router.add_route("POST", "/api/v1/refresh/", views.refresh)
    app.router.add_route("GET", "/api/v1/logout/", views.logout)
    app.router.add_route("GET", "/api/v1/login_taken/{username}/", views.login_taken)
    app.router.add_route("GET", "/api/v1/login_by_id/{id}/", views.get_login)
