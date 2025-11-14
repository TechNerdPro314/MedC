# app/schemas.py
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime, date
from typing import Optional
import re

phone_regex = re.compile(r"^\+?\d{7,15}$")


class PatientCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    gender: str
    date_of_birth: str
    address: str
    phone: str
    insurance_policy: str
    email: EmailStr
    age: Optional[int] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not phone_regex.match(value):
            raise ValueError(
                "Номер телефона не соответствует формату (от 7 до 15 цифр, может начинаться со знака +)."
            )
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):
        try:
            if "-" in value:
                dob = datetime.strptime(value, "%Y-%m-%d")
            else:
                dob = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                "Дата рождения должна быть в формате ДД.ММ.ГГГГ или YYYY-MM-DD"
            )
        return dob.strftime("%d.%m.%Y")

    @field_validator("age", mode="before")
    @classmethod
    def compute_age(cls, v, values):
        dob_str = values.data.get("date_of_birth")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%d.%m.%Y")
            except ValueError:
                # Если дата пришла в формате YYYY-MM-DD, парсим ее
                dob = datetime.strptime(dob_str, "%Y-%m-%d")

            today = datetime.now()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
            return age
        # Не выбрасываем ошибку, а возвращаем None, если возраст не может быть вычислен
        return None


class DoctorCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    cabinet: str
    specialization: str
    date_of_birth: str
    phone: str
    email: EmailStr
    workplace: str
    age: Optional[int] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not phone_regex.match(value):
            raise ValueError(
                "Номер телефона не соответствует формату (от 7 до 15 цифр, может начинаться со знака +)."
            )
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):
        try:
            if "-" in value:
                dob = datetime.strptime(value, "%Y-%m-%d")
            else:
                dob = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                "Дата рождения должна быть в формате ДД.ММ.ГГГГ или YYYY-MM-DD"
            )
        return dob.strftime("%d.%m.%Y")

    @field_validator("age", mode="before")
    @classmethod
    def compute_age(cls, v, values):
        dob_str = values.data.get("date_of_birth")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%d.%m.%Y")
            except ValueError:
                dob = datetime.strptime(dob_str, "%Y-%m-%d")

            today = datetime.now()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
            return age
        return None


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    service: str
    appointment_day: date
    appointment_time: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False


class User(UserBase):
    id: int
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
