# app/crud/doctor_crud.py
from sqlalchemy.orm import Session
from .. import models, schemas


def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    """
    Создает нового врача в базе данных.
    """
    # Создаем объект модели SQLAlchemy из данных Pydantic схемы
    # .model_dump() преобразует схему в словарь
    db_doctor = models.Doctor(**doctor.model_dump())

    # Явно устанавливаем вычисленное значение возраста
    db_doctor.age = doctor.age

    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
