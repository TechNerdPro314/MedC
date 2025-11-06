# app/routes/patient_routes.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal, engine

# Создаём таблицы, если они ещё не созданы
models.Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HTML-эндпоинты для регистрации пациента
@router.get("/register/patient", response_class=HTMLResponse)
def register_patient_form(request: Request):
    return templates.TemplateResponse("register_patient.html", {"request": request})

@router.post("/register/patient", response_class=HTMLResponse)
def register_patient(
    request: Request,
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(...),
    gender: str = Form(...),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    insurance_policy: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # Создаём объект схемы – здесь будет автоматически вычислен возраст и формат даты приведён к ДД.ММ.ГГГГ
    patient_data = schemas.PatientCreate(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        gender=gender,
        date_of_birth=date_of_birth,
        address=address,
        phone=phone,
        insurance_policy=insurance_policy,
        email=email
    )
    db_patient = models.Patient(**patient_data.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return RedirectResponse(url="/", status_code=302)

# API-эндпоинты для работы с пациентами
@router.post("/api/patients", response_model=schemas.PatientCreate)
def create_patient_api(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return patient

@router.get("/api/patients", response_model=list[schemas.PatientCreate])
def read_patients_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients
