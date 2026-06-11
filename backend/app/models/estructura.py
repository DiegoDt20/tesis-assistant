"""Modelo Estructura (nodo de jerarquía documental)."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Estructura(Base):
    __tablename__ = "estructuras"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    documento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documentos.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("estructuras.id", ondelete="CASCADE"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    jerarquia: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    contenido: Mapped[str | None] = mapped_column(Text, nullable=True)
    pagina_inicio: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    documento = relationship("Documento", back_populates="estructuras")
    hijos = relationship("Estructura", backref="parent", remote_side=[id])
