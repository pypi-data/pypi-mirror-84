"""
Security middlewares

Help project to enable security function faster and easy to config via settings
environment parameters.

Configs:
    - BACKEND_CORS_ORIGINS: List of CORS origins to enable CORS with them
"""
import pydantic
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def init_app(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    init_cors(app, settings)


def init_cors(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    if getattr(settings, "BACKEND_CORS_ORIGINS", None):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           getattr(settings, "BACKEND_CORS_ORIGINS")],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
