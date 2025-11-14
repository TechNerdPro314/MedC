# app/crud/patient_crud.py
from sqlalchemy.orm import Session
from .. import models, schemas


def create_patient(db: Session, patient: schemas.PatientCreate):
    """
    Создает нового пациента в базе данных.
    """
    # Создаем объект модели SQLAlchemy из данных Pydantic схемы
    db_patient = models.Patient(**patient.model_dump())

    # Явно устанавливаем вычисленное значение возраста
    db_patient.age = patient.age

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient_by_fullname(
    db: Session, last_name: str, first_name: str, patronymic: str | None = None
):
    """
    Находит пациента по полному имени.
    """
    query = db.query(models.Patient).filter(
        models.Patient.last_name == last_name, models.Patient.first_name == first_name
    )
    if patronymic:
        query = query.filter(models.Patient.patronymic == patronymic)

    return query.first()
