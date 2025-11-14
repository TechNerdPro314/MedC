from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from .. import models, schemas, auth
from ..crud import patient_crud
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/register/patient", response_class=HTMLResponse)
def register_patient_form(
    request: Request,
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
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
    # --- ДОБАВЛЕНЫ НОВЫЕ ПОЛЯ ИЗ ФОРМЫ ---
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
    patient_data = schemas.PatientCreate(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        gender=gender,
        date_of_birth=date_of_birth,
        address=address,
        phone=phone,
        insurance_policy=insurance_policy,
        email=email,
        # --- ПЕРЕДАЕМ ДАННЫЕ В СХЕМУ ---
        username=username if username else None,
        password=password if password else None,
    )
    patient_crud.create_patient(db=db, patient=patient_data)
    return RedirectResponse(url="/", status_code=302)


# ... (остальные эндпоинты файла без изменений)
@router.post("/api/patients", response_model=schemas.PatientCreate)
def create_patient_api(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
    db_patient = patient_crud.create_patient(db=db, patient=patient)
    return patient


@router.get("/api/patients", response_model=list[schemas.PatientCreate])
def read_patients_api(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return [schemas.PatientCreate.model_validate(p) for p in patients]
