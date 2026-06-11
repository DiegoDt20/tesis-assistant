"""Modelo Documento."""
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)  # guia/tesis_modelo/...
    ruta_archivo: Mapped[str] = mapped_column(Text, nullable=False)
    tamanio_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    paginas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="subido", nullable=False)
    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    usuario = relationship("Usuario", back_populates="documentos")
    estructuras = relationship(
        "Estructura", back_populates="documento", cascade="all, delete-orphan"
    )
    plantillas = relationship("Plantilla", back_populates="documento")