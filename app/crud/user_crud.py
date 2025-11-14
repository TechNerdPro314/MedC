# app/crud/user_crud.py
from passlib.context import CryptContext  # <-- Добавили импорт
from sqlalchemy.orm import Session

from .. import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Создает хеш из пароля."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль хешу."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str):
    """Находит пользователя по имени."""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    """Создает нового пользователя с хешированным паролем."""
    # Теперь эта функция вызывается из того же файла, импорт не нужен
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, hashed_password=hashed_password, is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
