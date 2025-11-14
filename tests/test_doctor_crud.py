# tests/test_doctor_crud.py
from app.crud import doctor_crud
from app.schemas import DoctorCreate


def test_create_doctor(test_db):
    """
    Тест для функции создания врача.
    """
    # Arrange
    doctor_data = DoctorCreate(
        last_name="Айболитов",
        first_name="Айболит",
        patronymic="Айболитович",
        cabinet="Кабинет 101",
        specialization="Терапевт",
        date_of_birth="01.01.1970",
        phone="+79001112233",
        email="aibolit@clinic.com",
        workplace="Адрес 1",
    )
    # Act
    db_doctor = doctor_crud.create_doctor(db=test_db, doctor=doctor_data)
    # Assert
    assert db_doctor.id is not None
    assert db_doctor.last_name == "Айболитов"
    assert db_doctor.specialization == "Терапевт"
    assert db_doctor.age is not None
