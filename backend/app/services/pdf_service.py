"""Servicio de extracción de texto desde PDF.

Usa pdfplumber por defecto; cae a PyMuPDF si falla.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class PaginaTexto:
    numero: int
    texto: str


@dataclass
class PDFExtractResult:
    paginas: list[PaginaTexto]
    texto_completo: str
    total_paginas: int


class PDFService:
    """Encapsula la extracción de texto del PDF."""

    def extract(self, pdf_path: str | Path) -> PDFExtractResult:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF no encontrado: {path}")

        try:
            return self._extract_with_pdfplumber(path)
        except Exception as e:  # noqa: BLE001
            log.warning("pdfplumber falló (%s), reintentando con PyMuPDF", e)
            return self._extract_with_pymupdf(path)

    # ---------- backends ----------
    def _extract_with_pdfplumber(self, path: Path) -> PDFExtractResult:
        import pdfplumber  # import perezoso

        paginas: list[PaginaTexto] = []
        with pdfplumber.open(str(path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                txt = page.extract_text() or ""
                paginas.append(PaginaTexto(numero=i, texto=txt))

        completo = "\n".join(p.texto for p in paginas)
        return PDFExtractResult(paginas=paginas, texto_completo=completo, total_paginas=len(paginas))

    def _extract_with_pymupdf(self, path: Path) -> PDFExtractResult:
        import fitz  # PyMuPDF

        paginas: list[PaginaTexto] = []
        doc = fitz.open(str(path))
        try:
            for i, page in enumerate(doc, start=1):
                paginas.append(PaginaTexto(numero=i, texto=page.get_text("text")))
        finally:
            doc.close()

        completo = "\n".join(p.texto for p in paginas)
        return PDFExtractResult(paginas=paginas, texto_completo=completo, total_paginas=len(paginas))
