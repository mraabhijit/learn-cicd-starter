import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# Convert libsql:// to sqlite:// or handle file: for SQLAlchemy
if DATABASE_URL:
    if DATABASE_URL.startswith("libsql://"):
        # For remote libsql, if user wants to use sqlalchemy, they usually
        # need a specific dialect or to use the local equivalent.
        # We'll leave it for now or assume they know what they're doing.
        pass
    elif DATABASE_URL.startswith("file:"):
        DATABASE_URL = DATABASE_URL.replace("file:", "sqlite:///", 1)
    elif DATABASE_URL.startswith("sqlite:"):
        # If it already starts with sqlite://, don't mangle it
        if not DATABASE_URL.startswith("sqlite://"):
            DATABASE_URL = DATABASE_URL.replace("sqlite:", "sqlite:///", 1)

# SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
