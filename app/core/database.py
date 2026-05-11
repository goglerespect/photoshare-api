from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Підключення до PostgreSQL
engine = create_engine(DATABASE_URL)

# Сесія
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Base для моделей
Base = declarative_base()


# Dependency для FastAPI
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()