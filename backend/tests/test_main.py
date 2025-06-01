import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

#
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_point():
    response = client.post("/add_point", json={
        "latitude": 42.7,
        "longitude": 23.3,
        "description": "Тестова точка"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == 42.7
    assert data["longitude"] == 23.3
    assert data["description"] == "Тестова точка"

def test_read_points():
    client.post("/add_point", json={
        "latitude": 42.7,
        "longitude": 23.3,
        "description": "Точка 1"
    })
    response = client.get("/points")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_update_point():
    r = client.post("/add_point", json={
        "latitude": 42.0,
        "longitude": 23.0,
        "description": "Update test"
    })
    point_id = r.json()["id"]
    response = client.put(f"/update_point/{point_id}", json={
        "latitude": 43.0,
        "longitude": 24.0,
        "description": "Обновена точка"
    })
    assert response.status_code == 200
    updated = response.json()
    assert updated["latitude"] == 43.0
    assert updated["description"] == "Обновена точка"

def test_delete_point():
    r = client.post("/add_point", json={
        "latitude": 42.0,
        "longitude": 23.0,
        "description": "Delete me"
    })
    point_id = r.json()["id"]
    response = client.delete(f"/delete_point/{point_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Point deleted"

    
    response = client.get("/points")
    assert len(response.json()) == 0
