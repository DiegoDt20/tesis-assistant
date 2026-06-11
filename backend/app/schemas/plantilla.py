"""Schemas Pydantic para Plantilla (DTOs de entrada y salida)."""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Esquema de una sección dentro de la plantilla
# ---------------------------------------------------------------------------

class SeccionSchema(BaseModel):
    """Una sección de la plantilla institucional."""
    id: str = Field(..., description="Identificador único de la sección, ej: 'resumen'")
    titulo: str = Field(..., description="Nombre de la sección, ej: 'Resumen'")
    obligatoria: bool = Field(default=True, description="Si la sección es requerida")
    orden: int = Field(..., description="Posición en el documento (1, 2, 3...)")
    hijos: list["SeccionSchema"] = Field(default_factory=list, description="Sub-secciones")

# Necesario para que SeccionSchema pueda referenciarse a sí misma
SeccionSchema.model_rebuild()


# ---------------------------------------------------------------------------
# Crear una plantilla manualmente
# ---------------------------------------------------------------------------

class PlantillaCreate(BaseModel):
    """Datos para crear una plantilla desde cero."""
    titulo: str = Field(..., min_length=3, max_length=200)
    secciones: list[SeccionSchema] = Field(..., min_length=1)
    documento_id: uuid.UUID | None = Field(
        default=None,
        description="ID del documento fuente (opcional)"
    )


# ---------------------------------------------------------------------------
# Crear plantilla desde un documento analizado
# ---------------------------------------------------------------------------

class PlantillaDesdeDocumento(BaseModel):
    """Crear plantilla automáticamente desde un documento ya analizado."""
    documento_id: uuid.UUID = Field(..., description="ID del documento analizado")
    titulo: str = Field(..., min_length=3, max_length=200)


# ---------------------------------------------------------------------------
# Respuesta de la API
# ---------------------------------------------------------------------------

class PlantillaResponse(BaseModel):
    """Plantilla devuelta por la API."""
    id: uuid.UUID
    usuario_id: uuid.UUID
    documento_id: uuid.UUID | None
    titulo: str
    secciones: list[SeccionSchema]
    fecha_creacion: datetime

    model_config = {"from_attributes": True}