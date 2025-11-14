from sqlalchemy.orm import Session
from datetime import date

from .. import models, schemas


def create_appointment(
    db: Session,
    appointment_day: date,
    appointment_time: str,
    patient_id: int,
    doctor_id: int,
    service: str,
):
    """
    Создает новую запись на прием в базе данных.
    """
    db_appointment = models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        service=service,
        appointment_day=appointment_day,
        appointment_time=appointment_time,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointments_by_patient_id(db: Session, patient_id: int):
    """
    Получает все записи на прием для конкретного пациента, объединяя с данными доктора.
    """
    return (
        db.query(models.Appointment)
        .join(models.Doctor)
        .filter(models.Appointment.patient_id == patient_id)
        .all()
    )
