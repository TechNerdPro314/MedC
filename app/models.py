from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String, index=True)
    date_of_birth = Column(String, index=True)  # хранится как строка
    address = Column(String, index=True)
    phone = Column(String, index=True)
    insurance_policy = Column(String, index=True)
    email = Column(String, index=True)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    cabinet = Column(String, index=True)
    specialization = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    age = Column(Integer)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    workplace = Column(String, index=True)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service = Column(String, index=True)
    appointment_day = Column(Date)
    appointment_time = Column(String)
    status = Column(String, default="Ожидание")
    diagnosis = Column(String)  # <--- Новый столбец 02.04.2025
    recommendations = Column(String)  # <--- Новый столбец 02.04.2025

    patient = relationship("Patient")# <--- Новый столбец 02.04.2025
    doctor = relationship("Doctor")# <--- Новый столбец 02.04.2025
    history = relationship("AppointmentHistory", back_populates="appointment")# <--- Новый столбец 02.04.2025

class AppointmentHistory(Base):
    __tablename__ = "appointment_history"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    old_status = Column(String, index=True)
    new_status = Column(String, index=True)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="history")

# <--- Обновлен 03.04.2025
class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    pharmacy_drug_id = Column(Integer, ForeignKey("pharmacy.id"), nullable=True)
    dosage = Column(String)

    patient = relationship("Patient")
    appointment = relationship("Appointment")
    pharmacy_drug = relationship("PharmacyDrug")


# <--- Новый класс 02.04.2025
class PatientDocument(Base):
    __tablename__ = "patient_documents"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    category = Column(String, default="Прочее")  # <--- добавлено
    filename = Column(String, index=True)
    original_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")

# <--- Новый класс 03.04.2025
class PharmacyDrug(Base):
    __tablename__ = "pharmacy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dosage = Column(String)
    instruction = Column(String)
    quantity = Column(Integer)

    def __repr__(self):
        return f"{self.name} ({self.dosage})"


