# app/crud/patient_crud.py
from sqlalchemy.orm import Session
from .. import models, schemas
from . import user_crud  # Импортируем CRUD пользователя


def create_patient(db: Session, patient: schemas.PatientCreate):
    """
    Создает нового пациента в базе данных.
    Если переданы username и password, также создает связанного пользователя.
    """
    new_user = None
    # 1. Если переданы данные для аккаунта, создаем пользователя
    if patient.username and patient.password:
        db_user = user_crud.get_user_by_username(db, username=patient.username)
        if db_user:
            # В реальном приложении здесь лучше выбрасывать HTTPException,
            # но для простоты пока оставим print.
            print(f"Пользователь с именем {patient.username} уже существует.")
            return None

        user_in = schemas.UserCreate(
            username=patient.username, password=patient.password
        )
        new_user = user_crud.create_user(db, user=user_in)

    # 2. Создаем пациента
    patient_dict = patient.model_dump(exclude={"username", "password"})
    db_patient = models.Patient(**patient_dict)
    db_patient.age = patient.age

    # 3. Если был создан пользователь, связываем его с пациентом
    if new_user:
        db_patient.user_id = new_user.id

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient_by_user_id(db: Session, user_id: int):
    """
    Находит профиль пациента по ID связанного с ним пользователя.
    """
    return db.query(models.Patient).filter(models.Patient.user_id == user_id).first()


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
