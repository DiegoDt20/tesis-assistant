from fastapi import APIRouter
from app.api.v1 import documentos, health, plantillas

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(documentos.router)
router.include_router(plantillas.router)