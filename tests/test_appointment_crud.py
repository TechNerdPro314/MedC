# tests/test_appointment_crud.py
from datetime import date
from app.crud import appointment_crud, patient_crud, doctor_crud
from app.schemas import PatientCreate, DoctorCreate


def test_create_and_get_appointment(test_db):
    """
    Тест для создания и последующего получения записи на прием.
    """
    # Arrange: Для создания записи нам сначала нужны пациент и врач в БД
    patient = patient_crud.create_patient(
        test_db,
        PatientCreate(
            last_name="Пациентов",
            first_name="Пётр",
            patronymic="Сидорович",
            gender="М",
            date_of_birth="11.11.1991",
            address="a",
            phone="+79123456789",
            insurance_policy="1112223334445556",
            email="e@e.com",
        ),
    )
    doctor = doctor_crud.create_doctor(
        test_db,
        DoctorCreate(
            last_name="Врачев",
            first_name="Василий",
            patronymic="Петрович",
            cabinet="1",
            specialization="Хирург",
            date_of_birth="10.10.1980",
            phone="+79998887766",
            email="d@d.com",
            workplace="w",
        ),
    )

    # Act: Создаем запись на прием
    appointment_date = date(2025, 12, 25)
    created_appointment = appointment_crud.create_appointment(
        db=test_db,
        patient_id=patient.id,
        doctor_id=doctor.id,
        service="Консультация",
        appointment_day=appointment_date,
        appointment_time="10:00",
    )
    # Assert: Проверяем, что запись создана корректно
    assert created_appointment.id is not None
    assert created_appointment.patient_id == patient.id
    assert created_appointment.doctor_id == doctor.id
    assert created_appointment.service == "Консультация"

    # Act: Теперь получаем все записи для этого пациента
    appointments_from_db = appointment_crud.get_appointments_by_patient_id(
        db=test_db, patient_id=patient.id
    )
    # Assert: Проверяем, что мы нашли нашу созданную запись
    assert len(appointments_from_db) == 1
    assert appointments_from_db[0].id == created_appointment.id
    assert (
        appointments_from_db[0].doctor.last_name == "Врачев"
    )  # Проверяем, что join сработал
