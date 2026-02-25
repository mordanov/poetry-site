"""
Database configuration and session management for Poetry Site
Uses SQLAlchemy ORM with SQLite
"""

import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import bcrypt
import uuid

from models import Base, Admin, About

load_dotenv()

# Database configuration
DB_PATH = os.getenv("DB_PATH", "/app/data/poetry.db")
UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

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


def _column_exists(db: Session, table: str, column: str) -> bool:
    rows = db.execute(text(f"PRAGMA table_info({table})")).fetchall()
    return any(row[1] == column for row in rows)


def _migrate_poems_schema(db: Session) -> None:
    if not _column_exists(db, "poems", "uuid"):
        db.execute(text("ALTER TABLE poems ADD COLUMN uuid VARCHAR(36)"))
    if not _column_exists(db, "poems", "image_filename"):
        db.execute(text("ALTER TABLE poems ADD COLUMN image_filename VARCHAR(255)"))
    if not _column_exists(db, "poems", "generation_id"):
        db.execute(text("ALTER TABLE poems ADD COLUMN generation_id VARCHAR(255)"))
    if not _column_exists(db, "poems", "is_draft"):
        db.execute(text("ALTER TABLE poems ADD COLUMN is_draft INTEGER DEFAULT 0 NOT NULL"))

    db.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_poems_uuid ON poems (uuid)"))
    db.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_poems_generation_id ON poems (generation_id) WHERE generation_id IS NOT NULL"))

    rows = db.execute(text("SELECT id FROM poems WHERE uuid IS NULL OR uuid = ''")).fetchall()
    for (poem_id,) in rows:
        db.execute(
            text("UPDATE poems SET uuid = :uuid WHERE id = :id"),
            {"uuid": str(uuid.uuid4()), "id": poem_id}
        )


def init_db():
    """
    Initialize database schema and seed default data
    Creates all tables and inserts default admin and about page
    """
    print("📊 Initializing database schema...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created/verified")

    # Apply lightweight migrations
    db = SessionLocal()
    try:
        _migrate_poems_schema(db)

        # Seed default data
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
