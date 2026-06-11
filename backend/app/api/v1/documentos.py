"""Endpoints de Documentos — Sprint 1."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas import DocumentoOut, DocumentoUploadResponse, EstructuraNode
from app.services import DocumentoService

router = APIRouter(prefix="/documentos", tags=["documentos"])
settings = get_settings()

# NOTA: en MVP usamos un usuario "demo" hasta implementar auth (Sprint 2/3).
DEMO_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


@router.post(
    "/upload",
    response_model=DocumentoUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_documento(
    file: UploadFile = File(...),
    tipo: str = "guia",
    db: Session = Depends(get_db),
) -> DocumentoUploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Solo se aceptan archivos .pdf")

    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Archivo supera {settings.max_upload_mb} MB")

    svc = DocumentoService(db)
    doc = svc.save_upload(DEMO_USER_ID, file.filename, content, tipo)
    secciones = svc.analizar(doc)

    nodos = [
        EstructuraNode(
            titulo=s.titulo,
            jerarquia=s.jerarquia,
            orden=s.orden,
            pagina_inicio=s.pagina_inicio,
        )
        for s in secciones
    ]
    return DocumentoUploadResponse(
        documento=DocumentoOut.model_validate(doc),
        estructura=nodos,
    )


@router.get("/{documento_id}", response_model=DocumentoOut)
def obtener_documento(documento_id: uuid.UUID, db: Session = Depends(get_db)) -> DocumentoOut:
    from app.models import Documento
    doc = db.get(Documento, documento_id)
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
    return DocumentoOut.model_validate(doc)
