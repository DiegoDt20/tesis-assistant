"""Schemas Pydantic — Estructura."""
import uuid

from pydantic import BaseModel, ConfigDict


class EstructuraBase(BaseModel):
    titulo: str
    jerarquia: int = 1
    orden: int
    pagina_inicio: int | None = None


class EstructuraOut(EstructuraBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    documento_id: uuid.UUID


class EstructuraNode(EstructuraBase):
    """Nodo jerárquico para devolver el árbol al frontend."""
    hijos: list["EstructuraNode"] = []
