from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import (
    appointment_router,
    archive_router,
    doctor_router,
    document_router,
    html_router,
    medication_router,
    patient_router,
    auth_router,
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
