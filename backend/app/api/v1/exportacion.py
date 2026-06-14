"""Rutas HTTP para Exportación — Sprint 5 + Auth."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.proyecto import Proyecto
from app.models.plantilla import Plantilla
from app.services.exportacion_service import exportar_a_docx

router = APIRouter(prefix="/exportacion", tags=["exportacion"])


# ---------------------------------------------------------------------------
# GET /exportacion/{proyecto_id}/docx
# Exporta el proyecto como archivo .docx descargable
# ---------------------------------------------------------------------------

@router.get("/{proyecto_id}/docx")
def exportar_docx(
    proyecto_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Exporta el proyecto completo como archivo .docx descargable."""
    # Obtener el proyecto verificando que pertenece al usuario
    proyecto = db.query(Proyecto).filter(
        Proyecto.id == proyecto_id,
        Proyecto.usuario_id == usuario.id,
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