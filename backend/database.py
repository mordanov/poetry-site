"""
Database configuration and session management for Poetry Site
Uses SQLAlchemy ORM with PostgreSQL
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import bcrypt

from models import Base, Admin, About

load_dotenv()

# Database configuration — requires DATABASE_URL (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")

# Ensure uploads directory exists
if not UPLOADS_DIR.startswith('/tmp'):  # Skip for test directories
    os.makedirs(UPLOADS_DIR, exist_ok=True)

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL logging
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    FastAPI dependency to get database session
    Automatically closes after request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database schema and seed default data.
    Creates all tables and inserts default admin and about page.
    """
    print("📊 Initializing database schema...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created/verified")

    db = SessionLocal()
    try:
        # Seed default admin
        default_username = os.getenv("ADMIN_USERNAME", "admin")
        default_password = os.getenv("ADMIN_PASSWORD", "changeme123")

        admin_exists = db.query(Admin).filter(Admin.username == default_username).first()
        if not admin_exists:
            hashed = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()
            admin = Admin(username=default_username, password_hash=hashed)
            db.add(admin)
            print(f"✅ Created default admin: {default_username}")
        else:
            print(f"ℹ️  Admin user '{default_username}' already exists")

        # Seed default about page
        about_exists = db.query(About).filter(About.id == 1).first()
        if not about_exists:
            poet_name = os.getenv('POET_NAME', 'Famous poet')
            about = About(
                id=1,
                name=poet_name,
                bio='Welcome to my poetry corner.'
            )
            db.add(about)
            print("✅ Created default about page")
        else:
            print("ℹ️  About page already exists")

        db.commit()
        print("✅ Database initialized successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        db.close()
