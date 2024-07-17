from fastapi import FastAPI
from core.config import settings
from api.base import api_router
from apps.base import app_router
# from db.session import Base
# from db.session import engine


def include_router(app):
    app.include_router(api_router)
    # app.include_router(app_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, description=settings.PROJECT_DESCRIPTION, version=settings.PROJECT_VERSION)
    include_router(app)
    return app

app = start_application()

# Base.metadata.create_all(bind=engine)
