from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.data.medications import medications_list

from .. import models
from ..data.medications import medications_list
from ..database import SessionLocal
from ..utils.generate_pdf import generate_medication_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/medications", response_class=HTMLResponse)
def medications_page(request: Request, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return templates.TemplateResponse(
        "medications.html",
        {
            "request": request,
            "patients": patients,
            "medications_list": medications_list,  # Передаём список лекарств
        },
    )


@router.get("/medications/{appointment_id}", response_class=HTMLResponse)
def view_medications(
    appointment_id: int, request: Request, db: Session = Depends(get_db)
):
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        return templates.TemplateResponse(
            "medication_details.html",
            {"request": request, "error": "Запись не найдена"},
        )

    medications = (
        db.query(models.Medication)
        .filter(models.Medication.appointment_id == appointment_id)
        .all()
    )

    return templates.TemplateResponse(
        "medication_details.html",
        {"request": request, "appointment": appointment, "medications": medications},
    )


@router.get("/generate_pdf/{appointment_id}")
def generate_pdf(appointment_id: int, db: Session = Depends(get_db)):
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not appointment:
        return {"error": "Запись не найдена"}

    patient = appointment.patient
    doctor = appointment.doctor
    medications = (
        db.query(models.Medication)
        .filter(models.Medication.appointment_id == appointment_id)
        .all()
    )

    # Генерация PDF
    pdf_path = generate_medication_pdf(patient, doctor, appointment, medications)

    return FileResponse(
        path=pdf_path, filename=pdf_path.split("/")[-1], media_type="application/pdf"
    )


@router.post("/add_medication")
def add_medication(
    patient_id: int = Form(...),
    appointment_id: int = Form(...),
    pharmacy_drug_id: int = Form(...),
    dosage: str = Form(...),
    db: Session = Depends(get_db),
):
    drug = db.query(models.PharmacyDrug).filter_by(id=pharmacy_drug_id).first()
    if not drug:
        return JSONResponse(content={"error": "Лекарство не найдено"}, status_code=404)

    if drug.quantity <= 0:
        return JSONResponse(content={"error": "Нет в наличии"}, status_code=400)

    # Списание
    drug.quantity -= 1

    medication = models.Medication(
        patient_id=patient_id,
        appointment_id=appointment_id,
        pharmacy_drug_id=pharmacy_drug_id,
        dosage=dosage,
    )
    db.add(medication)
    db.commit()

    return JSONResponse(content={"message": "Лекарство назначено и списано"})


@router.get("/get_appointments/{patient_id}")
def get_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.patient_id == patient_id)
        .all()
    )

    result = [
        {
            "id": a.id,
            "doctor": f"{a.doctor.last_name} {a.doctor.first_name} {a.doctor.patronymic}",
            "specialization": a.doctor.specialization,
            "service": a.service,
            "date": a.appointment_day.strftime("%d.%m.%Y"),
            "time": a.appointment_time,
        }
        for a in appointments
    ]

    return JSONResponse(content=result)


@router.get("/pharmacy", response_class=HTMLResponse)
def view_pharmacy(request: Request, search: str = "", db: Session = Depends(get_db)):
    query = db.query(models.PharmacyDrug)
    if search:
        query = query.filter(models.PharmacyDrug.name.ilike(f"%{search}%"))
    drugs = query.all()
    return templates.TemplateResponse(
        "pharmacy.html",
        {"request": request, "drugs": drugs, "medications_list": medications_list},
    )


@router.post("/pharmacy/add")
def add_pharmacy_drug(
    name: str = Form(...),
    dosage: str = Form(...),
    instruction: str = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
):
    new_drug = models.PharmacyDrug(
        name=name, dosage=dosage, instruction=instruction, quantity=quantity
    )
    db.add(new_drug)
    db.commit()
    return RedirectResponse(url="/pharmacy", status_code=303)


@router.post("/pharmacy/delete/{drug_id}")
def delete_pharmacy_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(models.PharmacyDrug).filter_by(id=drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Препарат не найден")

    db.delete(drug)
    db.commit()
    return RedirectResponse(url="/pharmacy", status_code=303)


@router.post("/pharmacy/restock/{drug_id}")
def restock(drug_id: int, quantity: int = Form(...), db: Session = Depends(get_db)):
    drug = db.query(models.PharmacyDrug).filter_by(id=drug_id).first()
    if drug:
        drug.quantity += quantity
        db.commit()
    return RedirectResponse(url="/pharmacy", status_code=303)
