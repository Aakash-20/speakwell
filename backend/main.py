from fastapi import FastAPI
from core.config import settings
from api.base import api_router
from apps.base import app_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="template/css"), name="static")
    app.mount("/image_gallery", StaticFiles(directory="template/gallery", check_dir=True), name="image_gallery")
    app.mount("/blogs_image", StaticFiles(directory="template/blog/images", check_dir=True), name="blogs_image")
    app.mount("/background", StaticFiles(directory="template/background"), name="background")


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, description=settings.PROJECT_DESCRIPTION, version=settings.PROJECT_VERSION)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
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
