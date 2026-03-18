"""Unit tests for backend API endpoints"""
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Must be set before importing app/database
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///:memory:'
os.environ['UPLOADS_DIR'] = '/tmp/test_uploads'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['POET_NAME'] = 'Test Poet'

from main import app
from database import Base, get_db
from models import Admin, Poem, About, Comment

# ── Async test engine ─────────────────────────────────────────────────────────
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# ─── Health Check Tests ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ─── Config Tests ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_config(client):
    response = await client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert data["poet_name"] == "Test Poet"

# ─── About Tests ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_about_empty(client):
    response = await client.get("/api/about")
    assert response.status_code == 200
    assert response.json() == {}

@pytest.mark.asyncio
async def test_get_about_with_data(client, db_session):
    db_session.add(About(id=1, name="Test Poet", bio="Test biography"))
    await db_session.commit()

    response = await client.get("/api/about")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Poet"
    assert data["bio"] == "Test biography"

# ─── Poems Tests ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_poems_empty(client):
    response = await client.get("/api/poems")
    assert response.status_code == 200
    data = response.json()
    assert data["poems"] == []
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_get_poems_with_data(client, db_session):
    import uuid
    db_session.add(Poem(uuid=str(uuid.uuid4()), title="Test Poem", body="Body", is_draft=False))
    await db_session.commit()

    response = await client.get("/api/poems")
    assert response.status_code == 200
    data = response.json()
    assert len(data["poems"]) == 1
    assert data["poems"][0]["title"] == "Test Poem"

@pytest.mark.asyncio
async def test_draft_poems_not_visible_to_public(client, db_session):
    import uuid
    db_session.add(Poem(uuid=str(uuid.uuid4()), title="Draft", body="Draft", is_draft=True))
    await db_session.commit()

    response = await client.get("/api/poems")
    assert response.status_code == 200
    assert response.json()["poems"] == []

# ─── Tags Tests ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_tags_empty(client):
    response = await client.get("/api/poems/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ─── Database Model Tests ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_poem_model_creation(db_session):
    import uuid
    from sqlalchemy import select
    db_session.add(Poem(uuid=str(uuid.uuid4()), title="Model Test", body="Testing ORM", is_draft=False))
    await db_session.commit()
    result = await db_session.execute(select(Poem).where(Poem.title == "Model Test"))
    p = result.scalar_one_or_none()
    assert p is not None
    assert p.body == "Testing ORM"

@pytest.mark.asyncio
async def test_about_model_creation(db_session):
    from sqlalchemy import select
    db_session.add(About(id=1, name="ORM Poet", bio="ORM Test"))
    await db_session.commit()
    result = await db_session.execute(select(About).where(About.id == 1))
    about = result.scalar_one_or_none()
    assert about is not None
    assert about.name == "ORM Poet"

@pytest.mark.asyncio
async def test_admin_model_creation(db_session):
    from sqlalchemy import select
    db_session.add(Admin(username="testadmin", password_hash="hashed"))
    await db_session.commit()
    result = await db_session.execute(select(Admin).where(Admin.username == "testadmin"))
    admin = result.scalar_one_or_none()
    assert admin is not None
    assert admin.password_hash == "hashed"

# ─── Comment Model Tests ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_comment_model_creation(db_session):
    import uuid
    from sqlalchemy import select
    poem = Poem(uuid=str(uuid.uuid4()), title="Poem", body="Test", is_draft=False)
    db_session.add(poem)
    await db_session.flush()

    db_session.add(Comment(poem_id=poem.id, author="User", body="Great!"))
    await db_session.commit()

    result = await db_session.execute(select(Comment).where(Comment.author == "User"))
    c = result.scalar_one_or_none()
    assert c is not None
    assert c.body == "Great!"

# ─── Data Integrity Tests ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_poem_delete_cascade(db_session):
    import uuid
    from sqlalchemy import select
    poem = Poem(uuid=str(uuid.uuid4()), title="To Delete", body="Test", is_draft=False)
    db_session.add(poem)
    await db_session.flush()
    db_session.add(Comment(poem_id=poem.id, author="User", body="Comment"))
    await db_session.commit()

    await db_session.delete(poem)
    await db_session.commit()

    result = await db_session.execute(select(Comment).where(Comment.poem_id == poem.id))
    assert result.scalars().all() == []

@pytest.mark.asyncio
async def test_poem_uuid_uniqueness(db_session):
    import uuid
    test_uuid = str(uuid.uuid4())
    db_session.add(Poem(uuid=test_uuid, title="First", body="Test", is_draft=False))
    await db_session.commit()

    db_session.add(Poem(uuid=test_uuid, title="Second", body="Test", is_draft=False))
    with pytest.raises(Exception):
        await db_session.commit()

# ─── Environment Variable Tests ───────────────────────────────────────────────

def test_poet_name_from_env():
    assert os.getenv("POET_NAME") == "Test Poet"

def test_database_url_from_env():
    database_url = os.getenv("DATABASE_URL")
    assert database_url is not None
    assert "sqlite" in database_url
