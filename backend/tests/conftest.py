import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_child():
    return {
        "name": "Bintang",
        "age_months": 18,
        "weight_kg": 11.2,
        "height_cm": 82.5,
    }
