# Arquitectura del Sistema — Tesis Assistant

## 1. Visión general

Sistema modular cliente-servidor para analizar y generar tesis académicas.
El **MVP** se centra en **extraer la estructura** de una guía/tesis modelo en PDF.

```
┌──────────────┐    HTTPS/JSON     ┌────────────────┐    SQL     ┌──────────────┐
│   Next.js    │ ────────────────► │   FastAPI      │ ─────────► │ PostgreSQL   │
│  (Frontend)  │ ◄──────────────── │   (Backend)    │ ◄───────── │              │
└──────────────┘                   └────────┬───────┘            └──────────────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ Servicios IA / │
                                   │ pdfplumber /   │
                                   │ spaCy / OpenAI │
                                   └────────────────┘
```

## 2. Diagrama de módulos

```mermaid
graph TB
    subgraph Frontend[Next.js 15 + TS + Tailwind]
        UI[UI Components]
        Pages[App Router Pages]
        SvcF[Services HTTP]
    end

    subgraph Backend[FastAPI + Python 3.11]
        API[API Layer v1]
        SvcB[Services Layer]
        Models[ORM Models]
        Schemas[Pydantic Schemas]
        DB[Database Layer]
        Core[Core / Config / Security]
    end

    subgraph IA[Procesamiento]
        PDF[pdfplumber / PyMuPDF]
        NLP[spaCy / regex]
        AI[OpenAI - Sprint 3+]
    end

    subgraph Persistencia
        PG[(PostgreSQL)]
        FS[Sistema de archivos /uploads]
    end

    UI --> Pages --> SvcF --> API
    API --> SvcB
    SvcB --> PDF
    SvcB --> NLP
    SvcB --> AI
    SvcB --> Models
    Models --> DB --> PG
    SvcB --> FS
    Core --> API
    Schemas --> API
```

## 3. Flujo MVP

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend (Next.js)
    participant B as Backend (FastAPI)
    participant P as PDFService
    participant S as StructureDetector
    participant D as PostgreSQL

    U->>F: Sube PDF
    F->>B: POST /api/v1/documents/upload
    B->>B: Guarda archivo en /uploads
    B->>D: INSERT documentos
    B->>P: extract_text(path)
    P-->>B: texto + páginas
    B->>S: detect_structure(texto)
    S-->>B: lista de secciones
    B->>D: INSERT estructuras (jerarquía)
    B-->>F: JSON con estructura detectada
    F-->>U: Renderiza checklist de capítulos
```

## 4. Capas (Clean Architecture light)

| Capa            | Responsabilidad                                    |
|-----------------|----------------------------------------------------|
| `api/`          | Rutas HTTP, validación de entrada/salida           |
| `schemas/`      | DTOs Pydantic (in/out)                             |
| `services/`     | Lógica de negocio (PDF, estructura, IA)            |
| `models/`       | Entidades SQLAlchemy                               |
| `database/`     | Sesión, engine, migraciones                        |
| `core/`         | Config, logging, seguridad                         |
| `utils/`        | Helpers transversales                              |

## 5. Roadmap por Sprints

- **Sprint 1** ✅ Subida PDF + detección estructural por regex.
- **Sprint 2** ⏳ Conversión estructura → plantilla JSON reutilizable.
- **Sprint 3** ⏳ Asistente conversacional (preguntas guiadas).
- **Sprint 4** ⏳ Generación automática de Resumen, Introducción, Objetivos (OpenAI).
- **Sprint 5** ⏳ Exportación a `.docx` con formato UCV.
