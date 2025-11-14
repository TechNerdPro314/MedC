# app/routes/doctor_routes.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# --- ДОБАВЛЕНЫ ИМПОРТЫ auth и schemas ---
from .. import models, schemas, auth
from ..crud import doctor_crud
from ..database import SessionLocal, engine
from ..data.specializations import specializations
from ..data.cabinets import cabinets

models.Base.metadata.create_all(bind=engine)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HTML-эндпоинты для регистрации врача
@router.get("/register/doctor", response_class=HTMLResponse)
def register_doctor_form(
    request: Request,
    # --- ДОБАВЛЕНА ЗАЩИТА: страницу может открыть только админ ---
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
    workplaces = ["Адрес 1", "Адрес 2", "Адрес 3"]
    return templates.TemplateResponse(
        "register_doctor.html",
        {
            "request": request,
            "workplaces": workplaces,
            "specializations": specializations,
            "cabinets": cabinets,
        },
    )


@router.post("/register/doctor", response_class=HTMLResponse)
def register_doctor(
    request: Request,
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(...),
    cabinet: str = Form(...),
    specialization: str = Form(...),
    date_of_birth: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    workplace: str = Form(...),
    db: Session = Depends(get_db),
    # --- ЗАЩИТА АДМИНИСТРАТОРОМ (уже была добавлена) ---
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
    doctor_data = schemas.DoctorCreate(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        cabinet=cabinet,
        specialization=specialization,
        date_of_birth=date_of_birth,
        phone=phone,
        email=email,
        workplace=workplace,
    )
    doctor_crud.create_doctor(db=db, doctor=doctor_data)
    return RedirectResponse(url="/", status_code=302)


# API-эндпоинты для работы с врачами
@router.post("/api/doctors", response_model=schemas.DoctorCreate)
def create_doctor_api(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    # --- ДОБАВЛЕНА ЗАЩИТА АДМИНИСТРАТОРОМ ---
    current_admin: schemas.User = Depends(auth.get_current_admin_user),
):
    db_doctor = doctor_crud.create_doctor(db=db, doctor=doctor)
    return doctor


@router.get("/api/doctors", response_model=list[schemas.DoctorCreate])
def read_doctors_api(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    # --- ДОБАВЛЕНА ЗАЩИТА (любой авторизованный пользователь) ---
    current_user: schemas.User = Depends(auth.get_current_user),
):
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return [schemas.DoctorCreate.model_validate(d) for d in doctors]
