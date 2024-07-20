from fastapi import FastAPI
from core.config import settings
from api.base import api_router
from apps.base import app_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from db.session import Base
# from db.session import engine


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="static/images"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, description=settings.PROJECT_DESCRIPTION, version=settings.PROJECT_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_application()

# Base.metadata.create_all(bind=engine)
