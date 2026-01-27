from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/spr_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

def get_db():
    """
    Dependency для FastAPI
    Отдаёт сессию и гарантирует закрытие
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()