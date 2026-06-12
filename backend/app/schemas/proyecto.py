"""Schemas Pydantic para Proyecto (DTOs de entrada y salida)."""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Crear un proyecto nuevo
# ---------------------------------------------------------------------------

class ProyectoCreate(BaseModel):
    """Datos para crear un proyecto nuevo."""
    titulo: str = Field(..., min_length=3, max_length=500)
    plantilla_id: uuid.UUID = Field(..., description="ID de la plantilla a seguir")


# ---------------------------------------------------------------------------
# Guardar respuesta de una sección
# ---------------------------------------------------------------------------

class RespuestaCreate(BaseModel):
    """Respuesta del usuario para una sección específica."""
    seccion_id: str = Field(..., description="ID de la sección, ej: 'resumen'")
    respuesta: str = Field(..., min_length=1, description="Texto de la respuesta")


# ---------------------------------------------------------------------------
# Respuesta de la API
# ---------------------------------------------------------------------------

class ProyectoResponse(BaseModel):
    """Proyecto devuelto por la API."""
    id: uuid.UUID
    usuario_id: uuid.UUID
    plantilla_id: uuid.UUID | None
    titulo: str
    estado: str
    respuestas: dict[str, str]
    fecha_creacion: datetime
    fecha_actualiz: datetime

    model_config = {"from_attributes": True}