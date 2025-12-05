"""Database configuration with flag-based PostgreSQL/MySQL selection."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from typing import Literal
from ..config import get_database_config

# Create base for models
Base = declarative_base()

def get_database_url() -> str:
    """Get database URL from config."""
    config = get_database_config()
    return config["url"]

def create_database_engine():
    """
    Create SQLAlchemy engine based on database type.

    Returns:
        SQLAlchemy engine or None if using JSON storage
    """
    config = get_database_config()
    db_type = config["type"]
    database_url = config["url"]

    if db_type == "json" or not database_url:
        return None

    # Create engine based on database type
    if db_type == "postgresql":
        engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections before using
            echo=False,  # Set to True for SQL debugging
        )
    elif db_type == "mysql":
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=False,
            pool_recycle=3600,  # Recycle connections after 1 hour
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return engine

# Create engine and session factory
# This is initialized at module level but depends on config
engine = None
SessionLocal = None

def init_db_engine():
    """Initialize the global engine and session factory."""
    global engine, SessionLocal
    engine = create_database_engine()
    if engine is not None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for FastAPI to get database session.

    Yields:
        Database session
    """
    if SessionLocal is None:
        # If called when DB is not configured, this is an error
        # But for hybrid usage, we might just return None?
        # Better to raise error as this should only be called if DB is active
        raise RuntimeError("Database not configured. Set DB_TYPE in .env")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Initialize database tables.
    Call this on application startup.
    """
    init_db_engine()
    
    if engine is None:
        print("Using JSON file storage (DB_TYPE=json)")
        return

    config = get_database_config()
    print(f"Initializing {config['type'].upper()} database...")

    # Import models to register them
    from . import models

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print(f"{config['type'].upper()} database initialized successfully!")
