"""Schemas Pydantic — Documento."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.estructura import EstructuraNode


class DocumentoBase(BaseModel):
    nombre: str
    tipo: str = "guia"


class DocumentoOut(DocumentoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    estado: str
    paginas: int | None = None
    fecha_subida: datetime


class DocumentoUploadResponse(BaseModel):
    documento: DocumentoOut
    estructura: list[EstructuraNode]
