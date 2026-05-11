from fastapi import FastAPI

from sqlalchemy.exc import OperationalError

import time

from app.core.database import Base
from app.core.database import engine

# Import models
from app.models.user import User

# Import routes
from app.routes.auth import router as auth_router


# FastAPI app
app = FastAPI(
    title="PhotoShare API"
)


# Waiting PostgreSQL startup
for i in range(10):

    try:

        # Create tables
        Base.metadata.create_all(bind=engine)

        print("Database connected!")

        break

    except OperationalError:

        print("Database not ready...")

        time.sleep(2)


# Connect routes
app.include_router(auth_router)


# Root endpoint
@app.get("/")
def root():

    return {
        "message": "PhotoShare API is working"
    }