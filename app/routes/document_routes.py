import os
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/uploads"


@router.get("/patients/{patient_id}/documents")
def show_documents(patient_id: int, request: Request, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter_by(id=patient_id).first()
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

    file_path = os.path.join(UPLOAD_DIR, str(patient_id), document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(document)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient_id}/documents", status_code=303)
