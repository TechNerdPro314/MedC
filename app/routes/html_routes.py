# app/routes/html_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models
from ..database import SessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Главная страница с отображением ближайших записей
@router.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    # Текущая дата
    today = datetime.now().date()
    # Дата через 7 дней
    next_week = today + timedelta(days=7)

    # Запрос к БД: получение записей на ближайшие 7 дней
    upcoming_appointments = db.query(models.Appointment).filter(
        models.Appointment.appointment_day >= today,
        models.Appointment.appointment_day <= next_week
    ).order_by(models.Appointment.appointment_day.asc()).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "upcoming_appointments": upcoming_appointments
    })

# Форма для записи на приём
@router.get("/appointment", response_class=HTMLResponse)
def appointment_form(request: Request):
    return templates.TemplateResponse("appointment.html", {"request": request})
