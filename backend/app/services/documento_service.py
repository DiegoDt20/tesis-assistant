"""Orquestador: persiste el documento y dispara el análisis estructural."""
from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models import Documento, Estructura
from app.services.pdf_service import PDFService
from app.services.structure_detector import StructureDetector, Seccion

log = get_logger(__name__)
settings = get_settings()


class DocumentoService:
    def __init__(
        self,
        db: Session,
        pdf_service: PDFService | None = None,
        detector: StructureDetector | None = None,
    ) -> None:
        self.db = db
        self.pdf_service = pdf_service or PDFService()
        self.detector = detector or StructureDetector()

    # ---------- Persistencia ----------
    def save_upload(self, usuario_id: uuid.UUID, filename: str, content: bytes, tipo: str) -> Documento:
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Nombre único en disco
        safe = f"{uuid.uuid4().hex}_{Path(filename).name}"
        path = upload_dir / safe
        path.write_bytes(content)

        doc = Documento(
            usuario_id=usuario_id,
            nombre=filename,
            tipo=tipo,
            ruta_archivo=str(path),
            tamanio_bytes=len(content),
            estado="subido",
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    # ---------- Análisis ----------
    def analizar(self, documento: Documento) -> list[Seccion]:
        documento.estado = "procesando"
        self.db.commit()

        try:
            extract = self.pdf_service.extract(documento.ruta_archivo)
            documento.paginas = extract.total_paginas
            secciones = self.detector.detect(extract)

            # Persistir
            for s in secciones:
                self.db.add(
                    Estructura(
                        documento_id=documento.id,
                        titulo=s.titulo,
                        jerarquia=s.jerarquia,
                        orden=s.orden,
                        pagina_inicio=s.pagina_inicio,
                    )
                )
            documento.estado = "analizado"
            self.db.commit()
            return secciones
        except Exception as e:  # noqa: BLE001
            log.exception("Error analizando documento %s", documento.id)
            documento.estado = "error"
            self.db.commit()
            raise
