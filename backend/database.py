"""
Database configuration and session management for Poetry Site
Uses SQLAlchemy ORM with SQLite
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import bcrypt

from models import Base, Admin, About

load_dotenv()

# Database configuration
DB_PATH = os.getenv("DB_PATH", "/app/data/poetry.db")

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Build SQLite database URL
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with SQLite optimizations
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)

# Enable SQLite performance optimizations
def _fk_pragma_on_connect(dbapi_conn, connection_record):
    """Enable foreign keys and optimize SQLite on connection"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
    cursor.execute("PRAGMA synchronous=NORMAL")  # Balance between safety and speed
    cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
    cursor.execute("PRAGMA temp_store=MEMORY")  # Use memory for temp tables
    cursor.close()

event.listen(engine, "connect", _fk_pragma_on_connect)

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
