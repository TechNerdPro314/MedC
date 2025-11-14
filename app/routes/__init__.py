from .patient_routes import router as patient_router
from .doctor_routes import router as doctor_router
from .html_routes import router as html_router
from .appointment_routes import router as appointment_router
from .medication_routes import router as medication_router
from .archive_routes import router as archive_router
from .document_routes import router as document_router
from .auth_routes import router as auth_router
from .profile_routes import router as profile_router


__all__ = [
    "patient_router",
    "doctor_router",
    "html_router",
    "appointment_router",
    "medication_router",
    "archive_router",
    "document_router",
    "auth_router",
    "profile_router",
]
