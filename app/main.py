from fastapi import FastAPI

from sqlalchemy.exc import OperationalError

import time

from app.core.database import Base
from app.core.database import engine

from app.models.user import User

app = FastAPI(
    title="PhotoShare API"
)

# Чекаємо поки PostgreSQL стартане
for i in range(10):

    try:

        Base.metadata.create_all(bind=engine)

        print("Database connected!")

        break

    except OperationalError:

        print("Database not ready...")

        time.sleep(2)


@app.get("/")
def root():

    return {
        "message": "PhotoShare API"
    }