"""Rutas HTTP para Generación de contenido — Sprint 4."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.proyecto import Proyecto
from app.models.plantilla import Plantilla
from app.services.generacion_service import generar_seccion, generar_todas_las_secciones

# Usuario demo
DEMO_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

router = APIRouter(prefix="/generacion", tags=["generacion"])


# ---------------------------------------------------------------------------
# POST /generacion/{proyecto_id}/seccion/{seccion_id}
# Genera el contenido de una sección específica
# ---------------------------------------------------------------------------

@router.post("/{proyecto_id}/seccion/{seccion_id}")
def generar_una_seccion(
    proyecto_id: uuid.UUID,
    seccion_id: str,
    db: Session = Depends(get_db),
):
    """Genera el contenido de una sección usando OpenAI."""
    # Obtener el proyecto
    proyecto = db.query(Proyecto).filter(
        Proyecto.id == proyecto_id,
        Proyecto.usuario_id == DEMO_USER_ID,
    ).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto {proyecto_id} no encontrado.",
        )

    # Obtener la plantilla
    plantilla = db.query(Plantilla).filter(
        Plantilla.id == proyecto.plantilla_id
    ).first()
    if not plantilla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla del proyecto no encontrada.",
        )

    # Generar el contenido
    try:
        contenido = generar_seccion(proyecto, plantilla, seccion_id)
        return {
            "proyecto_id": proyecto_id,
            "seccion_id": seccion_id,
            "contenido": contenido,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ---------------------------------------------------------------------------
# POST /generacion/{proyecto_id}/todas
# Genera el contenido de todas las secciones
# ---------------------------------------------------------------------------

@router.post("/{proyecto_id}/todas")
def generar_todo(
    proyecto_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Genera el contenido de todas las secciones del proyecto."""
    # Obtener el proyecto
    proyecto = db.query(Proyecto).filter(
        Proyecto.id == proyecto_id,
        Proyecto.usuario_id == DEMO_USER_ID,
    ).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto {proyecto_id} no encontrado.",
        )

    # Obtener la plantilla
    plantilla = db.query(Plantilla).filter(
        Plantilla.id == proyecto.plantilla_id
    ).first()
    if not plantilla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla del proyecto no encontrada.",
        )

    # Generar todas las secciones
    try:
        contenidos = generar_todas_las_secciones(proyecto, plantilla)
        return {
            "proyecto_id": proyecto_id,
            "secciones_generadas": contenidos,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )