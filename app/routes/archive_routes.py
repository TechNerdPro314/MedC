# app/routes/archive_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

# --- ДОБАВЛЕНЫ ИМПОРТЫ auth и schemas ---
from .. import models, auth, schemas
from ..database import SessionLocal

# --- ПРИМЕНЯЕМ ЗАЩИТУ КО ВСЕМУ РОУТЕРУ ---
router = APIRouter(dependencies=[Depends(auth.get_current_user)])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/archive", response_class=HTMLResponse)
def archive_page(
    request: Request,
    patient_id: int = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
):
    # Получаем список пациентов для выбора
    patients = db.query(models.Patient).all()
    today = datetime.now().date()

    # Если не выбран пациент или выбран "Все пациенты" (значение 0)
    if patient_id is None or patient_id == 0:
        query = db.query(models.Appointment).filter(
            models.Appointment.appointment_day < today
        )
    else:
        query = db.query(models.Appointment).filter(
            models.Appointment.patient_id == patient_id,
            models.Appointment.appointment_day < today,
        )

    # Сортировка по дате
    if sort == "asc":
        query = query.order_by(models.Appointment.appointment_day.asc())
    else:
        query = query.order_by(models.Appointment.appointment_day.desc())

    appointments = query.all()

    return templates.TemplateResponse(
        "archive.html",
        {
            "request": request,
            "patients": patients,
            "appointments": appointments,
            "selected_patient_id": patient_id,
            "sort": sort,
        },
    )
