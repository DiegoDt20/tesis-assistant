"""Rutas HTTP para Plantillas — Sprint 2 + Auth."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.plantilla import (
    PlantillaCreate,
    PlantillaDesdeDocumento,
    PlantillaResponse,
)
from app.services.plantilla_service import (
    crear_plantilla,
    crear_plantilla_desde_documento,
    listar_plantillas,
    obtener_plantilla,
    plantilla_a_response,
)

router = APIRouter(prefix="/plantillas", tags=["plantillas"])


@router.get("/", response_model=list[PlantillaResponse])
def listar(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    plantillas = listar_plantillas(db, usuario.id)
    return [plantilla_a_response(p) for p in plantillas]


@router.post("/", response_model=PlantillaResponse, status_code=status.HTTP_201_CREATED)
def crear(
    datos: PlantillaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    plantilla = crear_plantilla(db, usuario.id, datos)
    return plantilla_a_response(plantilla)


@router.post("/desde-documento", response_model=PlantillaResponse, status_code=status.HTTP_201_CREATED)
def crear_desde_documento(
    datos: PlantillaDesdeDocumento,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    try:
        plantilla = crear_plantilla_desde_documento(db, usuario.id, datos)
        return plantilla_a_response(plantilla)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{plantilla_id}", response_model=PlantillaResponse)
def obtener(
    plantilla_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    plantilla = obtener_plantilla(db, plantilla_id, usuario.id)
    if not plantilla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plantilla {plantilla_id} no encontrada.")
    return plantilla_a_response(plantilla)