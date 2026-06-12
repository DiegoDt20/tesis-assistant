"""Modelo Proyecto — trabajo concreto del estudiante."""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Usuario propietario del proyecto
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    # Plantilla institucional que sigue este proyecto
    plantilla_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plantillas.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Título de la investigación
    titulo: Mapped[str] = mapped_column(String(500), nullable=False)

    # Estado: borrador → en_progreso → completado
    estado: Mapped[str] = mapped_column(
        String(30), default="borrador", nullable=False
    )

    # Respuestas del usuario por sección:
    # { "resumen": "Mi investigación trata sobre...", "metodologia": "..." }
    respuestas_json: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    fecha_actualiz: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relaciones
    usuario = relationship("Usuario", back_populates="proyectos")
    plantilla = relationship("Plantilla", back_populates="proyectos")