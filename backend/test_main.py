"""Unit tests for backend API endpoints - Simplified version"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables before importing app
# DATABASE_URL must be set before database.py is imported
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['UPLOADS_DIR'] = '/tmp/test_uploads'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['POET_NAME'] = 'Test Poet'

from main import app
from database import Base, get_db
from models import Admin, Poem, About, Comment

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a database session for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Health Check Tests ───────────────────────────────────────────────────────

def test_health_check():
    """Test health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ─── Config Tests ─────────────────────────────────────────────────────────────

def test_get_config():
    """Test config endpoint returns poet name"""
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "poet_name" in data
    assert isinstance(data["poet_name"], str)
    assert data["poet_name"] == "Test Poet"


# ─── About Tests ──────────────────────────────────────────────────────────────

def test_get_about_empty():
    """Test getting about page when empty"""
    response = client.get("/api/about")
    assert response.status_code == 200
    data = response.json()
    assert data == {}


def test_get_about_with_data(db_session):
    """Test getting about page with data"""
    about = About(
        id=1,
        name="Test Poet",
        bio="Test biography"
    )
    db_session.add(about)
    db_session.commit()

    response = client.get("/api/about")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Poet"
    assert data["bio"] == "Test biography"


# ─── Poems Tests ──────────────────────────────────────────────────────────────

def test_get_poems_empty():
    """Test getting poems when database is empty"""
    response = client.get("/api/poems")
    assert response.status_code == 200
    data = response.json()
    assert data["poems"] == []
    assert data["total"] == 0


def test_get_poems_with_data(db_session):
    """Test getting poems with data"""
    import uuid
    poem = Poem(
        uuid=str(uuid.uuid4()),
        title="Test Poem",
        body="This is a test poem\nWith multiple lines",
        is_draft=False
    )
    db_session.add(poem)
    db_session.commit()

    response = client.get("/api/poems")
    assert response.status_code == 200
    data = response.json()
    assert len(data["poems"]) == 1
    assert data["poems"][0]["title"] == "Test Poem"


def test_draft_poems_not_visible_to_public(db_session):
    """Test that draft poems are not visible to public"""
    import uuid
    draft_poem = Poem(
        uuid=str(uuid.uuid4()),
        title="Draft Poem",
        body="Draft content",
        is_draft=True
    )
    db_session.add(draft_poem)
    db_session.commit()

    response = client.get("/api/poems")
    assert response.status_code == 200
    data = response.json()
    assert len(data["poems"]) == 0


# ─── Tags Tests ───────────────────────────────────────────────────────────────

def test_get_tags_empty():
    """Test getting tags when no poems exist"""
    response = client.get("/api/poems/tags")
    assert response.status_code == 200
    tags = response.json()
    assert isinstance(tags, (dict, list))


# ─── Database Model Tests ─────────────────────────────────────────────────────

def test_poem_model_creation(db_session):
    """Test creating poem via ORM model"""
    import uuid
    poem = Poem(
        uuid=str(uuid.uuid4()),
        title="Model Test",
        body="Testing ORM model",
        is_draft=False
    )
    db_session.add(poem)
    db_session.commit()

    retrieved = db_session.query(Poem).filter(Poem.title == "Model Test").first()
    assert retrieved is not None
    assert retrieved.body == "Testing ORM model"


def test_about_model_creation(db_session):
    """Test creating about page via ORM model"""
    about = About(
        id=1,
        name="ORM Poet",
        bio="ORM Test"
    )
    db_session.add(about)
    db_session.commit()

    retrieved = db_session.query(About).filter(About.id == 1).first()
    assert retrieved is not None
    assert retrieved.name == "ORM Poet"


def test_admin_model_creation(db_session):
    """Test creating admin via ORM model"""
    admin = Admin(
        username="testadmin",
        password_hash="hashed_password"
    )
    db_session.add(admin)
    db_session.commit()

    retrieved = db_session.query(Admin).filter(Admin.username == "testadmin").first()
    assert retrieved is not None
    assert retrieved.password_hash == "hashed_password"


# ─── Comment Model Tests ──────────────────────────────────────────────────────

def test_comment_model_creation(db_session):
    """Test creating comment via ORM model"""
    import uuid
    poem = Poem(
        uuid=str(uuid.uuid4()),
        title="Poem for Comments",
        body="Test",
        is_draft=False
    )
    db_session.add(poem)
    db_session.commit()

    comment = Comment(
        poem_id=poem.id,
        author="Test User",
        body="Great poem!"
    )
    db_session.add(comment)
    db_session.commit()

    retrieved = db_session.query(Comment).filter(Comment.author == "Test User").first()
    assert retrieved is not None
    assert retrieved.body == "Great poem!"
    assert retrieved.poem_id == poem.id


# ─── Data Integrity Tests ─────────────────────────────────────────────────────

def test_poem_delete_cascade(db_session):
    """Test that deleting a poem cascades to comments"""
    import uuid
    poem = Poem(
        uuid=str(uuid.uuid4()),
        title="To Delete",
        body="Test",
        is_draft=False
    )
    db_session.add(poem)
    db_session.commit()

    comment = Comment(
        poem_id=poem.id,
        author="User",
        body="Comment"
    )
    db_session.add(comment)
    db_session.commit()

    # Delete poem
    db_session.delete(poem)
    db_session.commit()

    # Verify comments are deleted
    remaining_comments = db_session.query(Comment).filter(Comment.poem_id == poem.id).all()
    assert len(remaining_comments) == 0


def test_poem_uuid_uniqueness(db_session):
    """Test that poem UUIDs are unique"""
    import uuid
    test_uuid = str(uuid.uuid4())

    poem1 = Poem(
        uuid=test_uuid,
        title="First",
        body="Test",
        is_draft=False
    )
    db_session.add(poem1)
    db_session.commit()

    # Try to create another with same UUID
    poem2 = Poem(
        uuid=test_uuid,
        title="Second",
        body="Test",
        is_draft=False
    )
    db_session.add(poem2)

    # Should raise IntegrityError
    with pytest.raises(Exception):
        db_session.commit()


# ─── Environment Variable Tests ───────────────────────────────────────────────

def test_poet_name_from_env():
    """Test that POET_NAME is read from environment"""
    poet_name = os.getenv("POET_NAME", "Famous poet")
    assert poet_name == "Test Poet"


def test_database_url_from_env():
    """Test that DATABASE_URL is read from environment"""
    database_url = os.getenv("DATABASE_URL")
    assert database_url is not None
    assert "sqlite" in database_url  # in-memory SQLite for tests
