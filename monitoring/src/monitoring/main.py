from fastapi import FastAPI

from .models import db

# from .rabbit import rabbit_init
from .views import init_app


def get_app():
    app = FastAPI(title="mailing service")
    db.init_app(app)
    init_app(app)
    # rabbit_init()
    return app
