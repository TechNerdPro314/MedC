# tests/test_user_crud.py
from app.crud import user_crud
from app.schemas import UserCreate


def test_password_hashing_and_verification(test_db):
    """
    Тест для проверки хеширования пароля и его верификации.
    Этот тест не использует БД, но мы передаем фикстуру для единообразия.
    """
    # Arrange
    plain_password = "mysecretpassword"
    # Act
    hashed_password = user_crud.get_password_hash(plain_password)
    # Assert
    assert hashed_password != plain_password
    assert user_crud.verify_password(plain_password, hashed_password)
    assert not user_crud.verify_password("wrongpassword", hashed_password)


def test_create_and_get_user(test_db):
    """
    Тест для создания и получения пользователя.
    """
    # Arrange
    user_data = UserCreate(username="testuser", password="password123", is_admin=False)
    # Act
    created_user = user_crud.create_user(db=test_db, user=user_data)
    # Assert
    assert created_user.id is not None
    assert created_user.username == "testuser"
    assert created_user.is_admin is False
    # Проверяем, что пароль в БД не равен исходному (т.е. он хеширован)
    assert created_user.hashed_password != "password123"

    # Act
    user_from_db = user_crud.get_user_by_username(db=test_db, username="testuser")
    # Assert
    assert user_from_db is not None
    assert user_from_db.username == created_user.username
