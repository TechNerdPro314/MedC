# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

# --- Настройка тестовой базы данных ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Используем БД в памяти
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы в тестовой БД перед запуском тестов
Base.metadata.create_all(bind=engine)


# --- "Фикстура" для предоставления сессии БД в тесты ---
@pytest.fixture()
def test_db():
    """
    Создает чистую сессию БД для одного теста.
    """
    db = TestingSessionLocal()
    try:
        yield db  # Предоставляет сессию тесту
    finally:
        db.close()  # Закрывает сессию после теста
