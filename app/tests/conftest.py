import pytest
from fastapi.testclient import TestClient
from app.main import app

# 1) Фікстура клієнта
@pytest.fixture(scope="session")
def client():
    return TestClient(app)

# 2) Автомок валідації породи, щоб не ходити в TheCatAPI
@pytest.fixture(autouse=True)
def mock_breed_validation(monkeypatch):
    async def _ok(*args, **kwargs) -> bool:
        return True
    from app.core import catapi
    monkeypatch.setattr(catapi, "validate_breed", _ok)
