"""Detector de estructura (capítulos / secciones) en una tesis o guía.

Heurísticas usadas:
  1. Numeración romana:   I.  II.  III.  IV.
  2. Numeración decimal:  1.  1.1  1.1.2
  3. Palabras clave académicas comunes en mayúsculas.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.services.pdf_service import PDFExtractResult


# ---- Patrones ----------------------------------------------------------------
ROMAN = r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
RE_ROMAN_HEAD = re.compile(rf"^\s*({ROMAN})\.\s+([A-ZÁÉÍÓÚÑ][^\n]{{2,120}})\s*$", re.MULTILINE)
RE_DECIMAL_HEAD = re.compile(r"^\s*(\d+(?:\.\d+){0,3})\.?\s+([A-ZÁÉÍÓÚÑ][^\n]{2,120})\s*$", re.MULTILINE)

KEYWORDS = [
    "RESUMEN", "ABSTRACT", "INTRODUCCIÓN", "INTRODUCCION",
    "OBJETIVOS", "JUSTIFICACIÓN", "JUSTIFICACION",
    "MARCO TEÓRICO", "MARCO TEORICO", "ESTADO DEL ARTE",
    "METODOLOGÍA", "METODOLOGIA", "MÉTODOS", "METODOS",
    "RESULTADOS", "DISCUSIÓN", "DISCUSION",
    "CONCLUSIONES", "RECOMENDACIONES",
    "REFERENCIAS", "BIBLIOGRAFÍA", "BIBLIOGRAFIA",
    "ANEXOS", "APÉNDICE", "APENDICE", "CRONOGRAMA",
]
RE_KEYWORD = re.compile(
    r"^\s*(" + "|".join(re.escape(k) for k in KEYWORDS) + r")\s*$",
    re.MULTILINE,
)


@dataclass
class Seccion:
    titulo: str
    jerarquia: int
    orden: int
    pagina_inicio: int | None = None
    hijos: list["Seccion"] = field(default_factory=list)


class StructureDetector:
    """Devuelve lista plana ordenada con la jerarquía detectada."""

    def detect(self, extract: PDFExtractResult) -> list[Seccion]:
        candidatos: list[tuple[int, int, str, int]] = []
        # (orden_aparicion_global, jerarquia, titulo, pagina)
        idx = 0
        for pag in extract.paginas:
            for match in RE_ROMAN_HEAD.finditer(pag.texto):
                titulo = match.group(5).strip()
                candidatos.append((idx, 1, self._fmt(match.group(1), titulo), pag.numero))
                idx += 1
            for match in RE_DECIMAL_HEAD.finditer(pag.texto):
                num, titulo = match.group(1), match.group(2).strip()
                jerarquia = num.count(".") + 1
                candidatos.append((idx, jerarquia, f"{num} {titulo}", pag.numero))
                idx += 1
            for match in RE_KEYWORD.finditer(pag.texto):
                candidatos.append((idx, 1, match.group(1).title(), pag.numero))
                idx += 1

        # Deduplicar por título normalizado, conservar primer match
        vistos: set[str] = set()
        unicos: list[tuple[int, int, str, int]] = []
        for c in candidatos:
            key = re.sub(r"\s+", " ", c[2]).strip().lower()
            if key in vistos:
                continue
            vistos.add(key)
            unicos.append(c)

        # Ordenar por aparición y asignar orden 1..N
        unicos.sort(key=lambda x: x[0])
        return [
            Seccion(titulo=t, jerarquia=j, orden=i + 1, pagina_inicio=p)
            for i, (_, j, t, p) in enumerate(unicos)
        ]

    @staticmethod
    def _fmt(romano: str, titulo: str) -> str:
        return f"{romano}. {titulo}"
