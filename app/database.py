# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Create the SQLAlchemy engine (handles connection)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creates a DB session factory that we’ll use in our routes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is our base class that all models will extend
Base = declarative_base()
