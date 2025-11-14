from app.crud import patient_crud
from app.schemas import PatientCreate
from app.models import Patient


def test_create_patient(test_db):
    """
    Тест для функции создания пациента.
    """
    # Arrange
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
    # Act
    db_patient = patient_crud.create_patient(db=test_db, patient=patient_data)
    # Assert
    assert db_patient.id is not None
    assert db_patient.last_name == "Тестов"
    assert db_patient.email == "test@example.com"
    assert db_patient.age is not None


def test_get_patient_by_fullname(test_db):
    """
    Тест для функции поиска пациента по ФИО.
    """
    # Arrange: Сначала создаем пациента, которого будем искать
    patient_data = PatientCreate(
        last_name="Иванов",
        first_name="Иван",
        patronymic="Иванович",
        gender="Мужской",
        date_of_birth="20.02.1985",
        address="Адрес",
        phone="+79234567890",
        insurance_policy="9876543210987654",
        email="ivan@test.com",
    )
    patient_crud.create_patient(db=test_db, patient=patient_data)

    # Act: Ищем созданного пациента
    found_patient = patient_crud.get_patient_by_fullname(
        db=test_db, last_name="Иванов", first_name="Иван", patronymic="Иванович"
    )
    # Assert: Проверяем, что пациент найден и его данные верны
    assert found_patient is not None
    assert found_patient.last_name == "Иванов"
    assert found_patient.patronymic == "Иванович"

    # Act: Ищем несуществующего пациента
    not_found_patient = patient_crud.get_patient_by_fullname(
        db=test_db, last_name="Петров", first_name="Петр", patronymic="Петрович"
    )
    # Assert: Проверяем, что функция вернула None
    assert not_found_patient is None
