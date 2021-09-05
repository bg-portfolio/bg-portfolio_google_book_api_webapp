import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.general_router import router


def include_router(app):
    app.include_router(router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_app():
    app = FastAPI()
    configure_static(app)
    include_router(app)
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = start_app()
