"""
Database configuration and session management for Poetry Site
Uses async SQLAlchemy ORM with asyncpg (PostgreSQL)
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import bcrypt

from models import Base, Admin, About

load_dotenv()

# DATABASE_URL must use postgresql+asyncpg:// scheme
# If a plain postgresql:// or postgresql+psycopg2:// URL is supplied
# we normalise it automatically so existing .env files keep working.
_raw_url = os.getenv("DATABASE_URL")
if not _raw_url:
    raise RuntimeError("DATABASE_URL environment variable is required")

if _raw_url.startswith("sqlite"):
    # Tests use SQLite in-memory via DATABASE_URL=sqlite+aiosqlite:///:memory:
    # Accept both bare sqlite:// and sqlite+aiosqlite://
    DATABASE_URL = _raw_url if "+aiosqlite" in _raw_url else _raw_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
elif _raw_url.startswith("postgresql://") or _raw_url.startswith("postgres://"):
    DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1).replace("postgres://", "postgresql+asyncpg://", 1)
elif _raw_url.startswith("postgresql+psycopg2://"):
    DATABASE_URL = _raw_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = _raw_url

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")

# Ensure uploads directory exists (skip for test /tmp dirs)
if not UPLOADS_DIR.startswith("/tmp"):
    os.makedirs(UPLOADS_DIR, exist_ok=True)

# ── Engine ────────────────────────────────────────────────────────────────────
if DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(DATABASE_URL, echo=False)
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# ── FastAPI dependency ────────────────────────────────────────────────────────
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# ── One-time init (called from lifespan) ─────────────────────────────────────
async def init_db():
    print("📊 Initializing database schema...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database schema created/verified")

    async with AsyncSessionLocal() as db:
        try:
            from sqlalchemy import select

            default_username = os.getenv("ADMIN_USERNAME", "admin")
            default_password = os.getenv("ADMIN_PASSWORD", "changeme123")

            result = await db.execute(select(Admin).where(Admin.username == default_username))
            admin_exists = result.scalar_one_or_none()
            if not admin_exists:
                hashed = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()
                db.add(Admin(username=default_username, password_hash=hashed))
                print(f"✅ Created default admin: {default_username}")
            else:
                print(f"ℹ️  Admin '{default_username}' already exists")

            result = await db.execute(select(About).where(About.id == 1))
            about_exists = result.scalar_one_or_none()
            if not about_exists:
                poet_name = os.getenv("POET_NAME", "Famous poet")
                db.add(About(id=1, name=poet_name, bio="Welcome to my poetry corner."))
                print("✅ Created default about page")
            else:
                print("ℹ️  About page already exists")

            await db.commit()
            print("✅ Database initialized successfully!")

        except Exception as e:
            await db.rollback()
            print(f"❌ Error initializing database: {e}")
            raise
