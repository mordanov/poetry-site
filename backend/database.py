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

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "poetry_db")
DB_USER = os.getenv("DB_USER", "poetry_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "poetry_password")

# Build database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connections before using
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
    Initialize database schema and seed default data
    Creates all tables and inserts default admin and about page
    """
    print("📊 Initializing database schema...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created/verified")

    # Seed default data
    db = SessionLocal()
    try:
        # Get admin credentials from environment
        default_username = os.getenv("ADMIN_USERNAME", "admin")
        default_password = os.getenv("ADMIN_PASSWORD", "changeme123")

        # Check if admin exists
        admin_exists = db.query(Admin).filter(Admin.username == default_username).first()
        if not admin_exists:
            hashed = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()
            admin = Admin(username=default_username, password_hash=hashed)
            db.add(admin)
            print(f"✅ Created default admin: {default_username}")
        else:
            print(f"ℹ️  Admin user '{default_username}' already exists")

        # Check if about page exists
        about_exists = db.query(About).filter(About.id == 1).first()
        if not about_exists:
            about = About(
                id=1,
                name='Lev Gorev',
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
