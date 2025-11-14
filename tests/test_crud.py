# tests/test_crud.py
from app.crud import patient_crud
from app.schemas import PatientCreate
from app.models import Patient


def test_create_patient(test_db):
    """
    Тест для функции создания пациента.
    'test_db' - это фикстура из conftest.py, она предоставляет чистую сессию.
    """
    # 1. Arrange (Подготовка): создаем данные для нового пациента
    # Pydantic-схема автоматически обработает дату и вычислит возраст.
    patient_data = PatientCreate(
        last_name="Тестов",
        first_name="Тест",
        patronymic="Тестович",
        gender="Мужской",
        date_of_birth="15.01.1990",
        address="г. Тестовый, ул. Программная, 1",
        phone="+79991234567",
        insurance_policy="1234567890123456",
        email="test@example.com",
    )

    # 2. Act (Действие): вызываем тестируемую функцию
    db_patient = patient_crud.create_patient(db=test_db, patient=patient_data)

    # 3. Assert (Проверка): убеждаемся, что результат соответствует ожиданиям
    assert db_patient.id is not None  # Убеждаемся, что БД присвоила ID
    assert db_patient.last_name == "Тестов"
    assert db_patient.first_name == "Тест"
    assert db_patient.email == "test@example.com"
    assert db_patient.age is not None  # Убеждаемся, что возраст был вычислен

    # Дополнительная проверка: убедимся, что запись действительно есть в БД
    patient_in_db = test_db.query(Patient).filter(Patient.id == db_patient.id).first()
    assert patient_in_db is not None
    assert patient_in_db.last_name == "Тестов"
