from datetime import datetime

from sqlalchemy import (  # Добавили Text
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), index=True)
    first_name = Column(String(100), index=True)
    patronymic = Column(String(100), index=True)
    age = Column(Integer)
    gender = Column(String(50), index=True)
    date_of_birth = Column(String(50), index=True)
    address = Column(String(255), index=True)
    phone = Column(String(50), index=True)
    insurance_policy = Column(String(50), index=True)
    email = Column(String(100), index=True)


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), index=True)
    first_name = Column(String(100), index=True)
    patronymic = Column(String(100), index=True)
    cabinet = Column(String(100), index=True)
    specialization = Column(String(100), index=True)
    date_of_birth = Column(String(50), index=True)
    age = Column(Integer)
    phone = Column(String(50), index=True)
    email = Column(String(100), index=True)
    workplace = Column(String(255), index=True)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service = Column(String(255), index=True)
    appointment_day = Column(Date)
    appointment_time = Column(String(50))
    status = Column(String(50), default="Ожидание")
    diagnosis = Column(Text)  # Используем Text для длинных описаний
    recommendations = Column(Text)  # Используем Text для длинных описаний

    patient = relationship("Patient")
    doctor = relationship("Doctor")
    history = relationship("AppointmentHistory", back_populates="appointment")


class AppointmentHistory(Base):
    __tablename__ = "appointment_history"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    old_status = Column(String(50), index=True)
    new_status = Column(String(50), index=True)
    reason = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="history")


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    pharmacy_drug_id = Column(Integer, ForeignKey("pharmacy.id"), nullable=True)
    dosage = Column(String(255))

    patient = relationship("Patient")
    appointment = relationship("Appointment")
    pharmacy_drug = relationship("PharmacyDrug")


class PatientDocument(Base):
    __tablename__ = "patient_documents"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    category = Column(String(100), default="Прочее")
    filename = Column(String(255), index=True)
    original_name = Column(String(255))
    upload_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")


class PharmacyDrug(Base):
    __tablename__ = "pharmacy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    dosage = Column(String(255))
    instruction = Column(Text)
    quantity = Column(Integer)

    def __repr__(self):
        return f"{self.name} ({self.dosage})"
