from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import (
    patient_router,
    doctor_router,
    html_router,
    appointment_router,
    medication_router,
    archive_router,
    document_router,
    auth_router,
    profile_router,
)

app = FastAPI(title="Медицинская организация")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(html_router)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(medication_router)
app.include_router(archive_router)
app.include_router(document_router)
app.include_router(auth_router)
app.include_router(profile_router)
