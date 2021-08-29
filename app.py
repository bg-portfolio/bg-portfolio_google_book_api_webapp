from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.general_router import router


def include_router(app):
    app.include_router(router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_app():
    app = FastAPI()
    include_router(app)
    configure_static(app)
    return app


app = start_app()
