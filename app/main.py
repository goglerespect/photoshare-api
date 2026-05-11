from fastapi import FastAPI

from sqlalchemy.exc import OperationalError

import time

from app.core.database import Base
from app.core.database import engine

from app.models.user import User

from app.routes.auth import router as auth_router

app = FastAPI(
    title="PhotoShare API"
)

# Retry для PostgreSQL
for i in range(10):

    try:

        Base.metadata.create_all(bind=engine)

        print("Database connected!")

        break

    except OperationalError:

        print("Database not ready...")

        time.sleep(2)

# Routes
app.include_router(auth_router)


@app.get("/")
def root():

    return {
        "message": "PhotoShare API"
    }