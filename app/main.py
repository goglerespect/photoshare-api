from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlalchemy.exc import OperationalError

import time

# Database
from app.core.database import Base
from app.core.database import engine

# Models
from app.models.user import User
from app.models.photo import Photo
from app.models.comment import Comment
from app.models.tag import Tag
from app.models.photo_tag import photo_tags
from app.models.transformation import Transformation

# Routes
from app.routes.auth import router as auth_router
from app.routes.photos import router as photos_router
from app.routes.comments import router as comments_router
from app.routes.users import router as users_router
from app.routes.test import router as test_router


# FastAPI app
app = FastAPI(
    title="PhotoShare API"
)


# Waiting PostgreSQL startup
for i in range(10):

    try:

        # Create database tables
        Base.metadata.create_all(bind=engine)

        print("Database connected!")

        break

    except OperationalError:

        print("Database not ready...")

        time.sleep(2)


# Routes
app.include_router(auth_router)

app.include_router(photos_router)

app.include_router(comments_router)

app.include_router(users_router)

app.include_router(test_router)


# Static uploads
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# Root endpoint
@app.get("/")
def root():

    return {
        "message": "PhotoShare API is working"
    }