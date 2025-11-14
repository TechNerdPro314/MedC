# app/routes/document_routes.py
from fastapi import APIRouter, UploadFile, Form, Request, Depends, HTTPException, File
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os, shutil

# --- ДОБАВЛЕНЫ ИМПОРТЫ auth и schemas ---
from .. import models, auth, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates

# --- ПРИМЕНЯЕМ ЗАЩИТУ КО ВСЕМУ РОУТЕРУ ---
router = APIRouter(dependencies=[Depends(auth.get_current_user)])
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/uploads"


@router.get("/patients/{patient_id}/documents")
def show_documents(patient_id: int, request: Request, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter_by(id=patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Пациент не найден")

    documents = db.query(models.PatientDocument).filter_by(patient_id=patient_id).all()
    return templates.TemplateResponse(
        "patient_documents.html",
        {"request": request, "patient": patient, "documents": documents},
    )


@router.post("/patients/{patient_id}/documents")
async def upload_document(
    patient_id: int,
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    category = category.strip().capitalize()
    category_path = os.path.join(UPLOAD_DIR, str(patient_id), category)
    os.makedirs(category_path, exist_ok=True)

    filename = f"{datetime.now().timestamp()}_{file.filename}"
    file_path = os.path.join(category_path, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = models.PatientDocument(
        patient_id=patient_id,
        filename=filename,
        original_name=file.filename,
        category=category,
    )
    db.add(document)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}/documents", status_code=303)


@router.post("/patients/{patient_id}/documents/{doc_id}/delete")
def delete_document(patient_id: int, doc_id: int, db: Session = Depends(get_db)):
    document = (
        db.query(models.PatientDocument)
        .filter_by(id=doc_id, patient_id=patient_id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # Формируем путь к файлу с учетом категории
    file_path = os.path.join(
        UPLOAD_DIR, str(patient_id), document.category, document.filename
    )
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(document)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}/documents", status_code=303)
