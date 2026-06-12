"""Rutas HTTP para Exportación — Sprint 5."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.proyecto import Proyecto
from app.models.plantilla import Plantilla
from app.services.exportacion_service import exportar_a_docx

# Usuario demo
DEMO_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

router = APIRouter(prefix="/exportacion", tags=["exportacion"])


@router.get("/{proyecto_id}/docx")
def exportar_docx(
    proyecto_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Exporta el proyecto completo como archivo .docx descargable."""
    # Obtener el proyecto
    proyecto = db.query(Proyecto).filter(
        Proyecto.id == proyecto_id,
        Proyecto.usuario_id == DEMO_USER_ID,
    ).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    # Obtener la plantilla
    plantilla = db.query(Plantilla).filter(
        Plantilla.id == proyecto.plantilla_id
    ).first()
    if not plantilla:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada.")

    # Generar el docx
    contenido = exportar_a_docx(proyecto, plantilla)

    # Nombre del archivo
    nombre = f"{proyecto.titulo[:50].replace(' ', '_')}.docx"

    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={nombre}"},
    )