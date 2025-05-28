from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database file inside the project folder
# app/database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/sqlite3.db"

# Create engine (check_same_thread=False is needed for SQLite in FastAPI)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Session for DB operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import User  # Import models to ensure they are registered
    Base.metadata.create_all(bind=engine)


