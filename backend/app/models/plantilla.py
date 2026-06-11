"""Modelo Plantilla — representa una estructura institucional reutilizable."""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base


class Plantilla(Base):
    __tablename__ = "plantillas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Usuario propietario de la plantilla
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    # Documento fuente del que se extrajo (opcional)
    documento_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documentos.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Nombre descriptivo de la plantilla
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)

    # Secciones en formato JSON:
    # [{"id": "resumen", "titulo": "Resumen", "obligatoria": true, "orden": 1}, ...]
    secciones_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relaciones
    usuario = relationship("Usuario", back_populates="plantillas")
    documento = relationship("Documento", back_populates="plantillas")