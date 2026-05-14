import os

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.core.database import (
    Base,
    engine
)

from app.routes.auth import router as auth_router
from app.routes.photos import router as photos_router
from app.routes.comments import router as comments_router
from app.routes.users import router as users_router
from app.routes.ratings import router as ratings_router
from app.routes.test import router as test_router


# CREATE TABLES
Base.metadata.create_all(
    bind=engine
)


# CREATE FASTAPI APP
app = FastAPI(
    title="PhotoShare API"
)


# CREATE UPLOADS DIRECTORY
os.makedirs(
    "uploads",
    exist_ok=True
)


# STATIC FILES
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# INCLUDE ROUTERS
app.include_router(auth_router)

app.include_router(photos_router)

app.include_router(comments_router)

app.include_router(users_router)

app.include_router(ratings_router)

app.include_router(test_router)


# ROOT ENDPOINT
@app.get("/")
def root():

    return {
        "message": "PhotoShare API is running"
    }


# HEALTHCHECK
@app.get("/health")
def healthcheck():

    return {
        "status": "ok"
    }