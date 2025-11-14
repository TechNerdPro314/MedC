from sqlalchemy.orm import Session

from .. import models, schemas


def create_patient(db: Session, patient: schemas.PatientCreate):
    """
    Создает нового пациента в базе данных.
    """
    # 1. Создаем объект модели SQLAlchemy из данных Pydantic схемы
    db_patient = models.Patient(**patient.dict())

    # 2. Добавляем объект в сессию (готовим к сохранению)
    db.add(db_patient)

    # 3. Сохраняем изменения в базе данных
    db.commit()

    # 4. Обновляем объект, чтобы получить ID, присвоенный базой данных
    db.refresh(db_patient)

    # 5. Возвращаем созданный объект пациента
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
