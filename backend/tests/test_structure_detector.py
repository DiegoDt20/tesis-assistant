"""Tests unitarios del StructureDetector."""
from app.services.pdf_service import PaginaTexto, PDFExtractResult
from app.services.structure_detector import StructureDetector


SAMPLE = """
I. Resumen
Texto del resumen.

II. Introducción
Contenido.

1. Objetivos
1.1 Objetivo general
1.2 Objetivos específicos

METODOLOGÍA
"""


def test_detect_basic():
    extract = PDFExtractResult(
        paginas=[PaginaTexto(numero=1, texto=SAMPLE)],
        texto_completo=SAMPLE,
        total_paginas=1,
    )
    secciones = StructureDetector().detect(extract)
    titulos = [s.titulo for s in secciones]

    assert any("Resumen" in t for t in titulos)
    assert any("Introducción" in t for t in titulos)
    assert any("Objetivos" in t for t in titulos)
    assert any("Metodología" in t.lower() or "METODOLOGÍA" in t for t in titulos)
