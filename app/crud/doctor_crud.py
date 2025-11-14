from sqlalchemy.orm import Session

from .. import models, schemas


def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    """
    Создает нового врача в базе данных.
    """
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
