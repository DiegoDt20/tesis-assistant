"""Rutas HTTP para Proyectos — Sprint 3 + Auth."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.proyecto import ProyectoCreate, RespuestaCreate, ProyectoResponse
from app.services.proyecto_service import (
    crear_proyecto,
    guardar_respuesta,
    listar_proyectos,
    obtener_proyecto,
    proyecto_a_response,
)

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


# ---------------------------------------------------------------------------
# GET /proyectos — listar todos los proyectos del usuario
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[ProyectoResponse])
def listar(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Lista todos los proyectos del usuario actual."""
    proyectos = listar_proyectos(db, usuario.id)
    return [proyecto_a_response(p) for p in proyectos]


# ---------------------------------------------------------------------------
# POST /proyectos — crear proyecto nuevo
# ---------------------------------------------------------------------------

@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def crear(
    datos: ProyectoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Crea un nuevo proyecto asociado a una plantilla."""
    try:
        proyecto = crear_proyecto(db, usuario.id, datos)
        return proyecto_a_response(proyecto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------------------------------------------------------------------------
# GET /proyectos/{id} — obtener un proyecto específico
# ---------------------------------------------------------------------------

@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener(
    proyecto_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Obtiene un proyecto por su ID."""
    proyecto = obtener_proyecto(db, proyecto_id, usuario.id)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto {proyecto_id} no encontrado.",
        )
    return proyecto_a_response(proyecto)


# ---------------------------------------------------------------------------
# POST /proyectos/{id}/respuestas — guardar respuesta de una sección
# ---------------------------------------------------------------------------

@router.post("/{proyecto_id}/respuestas", response_model=ProyectoResponse)
def responder(
    proyecto_id: uuid.UUID,
    datos: RespuestaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Guarda la respuesta del usuario para una sección específica.
    Este es el corazón del asistente conversacional.
    """
    try:
        proyecto = guardar_respuesta(db, usuario.id, proyecto_id, datos)
        return proyecto_a_response(proyecto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))