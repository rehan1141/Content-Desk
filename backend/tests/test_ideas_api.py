import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_quick_capture_api():
    """Test POST /api/v1/inbox/quick-capture creates raw thought."""
    response = client.post(
        "/api/v1/inbox/quick-capture",
        json={"raw_thought": "I realized I don't hate scripting. I hate scripts that don't sound like me."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["raw_thought"] == "I realized I don't hate scripting. I hate scripts that don't sound like me."
    assert data["status"] == "RAW"
    assert data["id"] is not None


def test_quick_capture_validation_error():
    """Test quick capture rejects empty thoughts."""
    response = client.post(
        "/api/v1/inbox/quick-capture",
        json={"raw_thought": "   "}
    )
    assert response.status_code == 400


def test_list_inbox_thoughts_api():
    """Test GET /api/v1/inbox lists thoughts sitting in inbox."""
    client.post("/api/v1/inbox/quick-capture", json={"raw_thought": "Thought 1"})
    client.post("/api/v1/inbox/quick-capture", json={"raw_thought": "Thought 2"})

    response = client.get("/api/v1/inbox")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_and_update_idea_api():
    """Test creating structured idea and updating status & development prompts."""
    create_res = client.post(
        "/api/v1/ideas",
        json={
            "raw_thought": "Why students don't need more study motivation.",
            "title": "Motivation vs Discipline",
            "status": "RAW"
        }
    )
    assert create_res.status_code == 201
    idea_id = create_res.json()["id"]

    # Update idea status & prompts
    update_res = client.patch(
        f"/api/v1/ideas/{idea_id}",
        json={
            "status": "DEVELOPING",
            "why_prompt": "Because students lack clarity, not motivation.",
            "development_notes": "Use college study abroad experience as an example."
        }
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["status"] == "DEVELOPING"
    assert updated_data["why_prompt"] == "Because students lack clarity, not motivation."
    assert updated_data["development_notes"] == "Use college study abroad experience as an example."


def test_filter_ideas_by_status_api():
    """Test GET /api/v1/ideas?status=DEVELOPING filters correctly."""
    client.post("/api/v1/inbox/quick-capture", json={"raw_thought": "Raw thought 1"})
    create_res = client.post(
        "/api/v1/ideas",
        json={"raw_thought": "Developing idea 1", "status": "DEVELOPING"}
    )
    idea_id = create_res.json()["id"]

    response = client.get("/api/v1/ideas?status=DEVELOPING")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == idea_id


def test_delete_idea_api():
    """Test DELETE /api/v1/ideas/{idea_id} permanently removes idea."""
    create_res = client.post("/api/v1/inbox/quick-capture", json={"raw_thought": "To be deleted"})
    idea_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/ideas/{idea_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/v1/ideas/{idea_id}")
    assert get_res.status_code == 404
