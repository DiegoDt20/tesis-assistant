# Tesis Assistant — MVP

Asistente inteligente para tesis universitarias.
**MVP (Sprint 1):** subir un PDF (guía o tesis modelo) y detectar automáticamente su estructura jerárquica.

---

## Arquitectura

```
Frontend (Next.js 15 + TS + Tailwind)
        │
        ▼  HTTP / JSON
Backend (FastAPI + Python 3.11)
   ├── Servicios: PDF, StructureDetector, Documento
   ├── Modelos SQLAlchemy
   └── PostgreSQL
```

Detalle completo en [`docs/01-arquitectura.md`](docs/01-arquitectura.md).
Esquema SQL en [`docs/02-base-datos.sql`](docs/02-base-datos.sql).

---

## Estructura de carpetas

```
tesis-assistant/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # Rutas HTTP versionadas
│   │   ├── core/           # Config, logging
│   │   ├── database/       # Engine, sesión, Base
│   │   ├── models/         # ORM SQLAlchemy
│   │   ├── schemas/        # DTOs Pydantic
│   │   ├── services/       # Lógica (PDF, detector, documento)
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   ├── uploads/            # PDFs subidos
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/                # App Router (Next.js 15)
│   │   ├── upload/
│   │   ├── dashboard/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/             # Botones, inputs reutilizables
│   │   └── analysis/       # StructureList, etc.
│   ├── services/           # Cliente HTTP
│   ├── types/              # Tipos compartidos
│   ├── package.json
│   └── tsconfig.json
│
├── docs/
│   ├── 01-arquitectura.md
│   └── 02-base-datos.sql
│
└── scripts/
    └── init_db.sh
```

---

## Cómo correr el MVP

### 1. Base de datos

```bash
createdb tesis_assistant
psql -d tesis_assistant -f docs/02-base-datos.sql
```

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # ajusta DATABASE_URL
uvicorn app.main:app --reload --port 8000
```

API en `http://localhost:8000/docs`.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

UI en `http://localhost:3000`.

---

## Roadmap

| Sprint | Objetivo                                        | Estado |
|--------|-------------------------------------------------|--------|
| 1      | Subir PDF + detectar estructura                 | ✅     |
| 2      | Estructura → plantilla JSON reutilizable        | ⏳     |
| 3      | Asistente conversacional (preguntas guiadas)    | ⏳     |
| 4      | Generación automática de secciones (OpenAI)     | ⏳     |
| 5      | Exportar a `.docx` con formato UCV              | ⏳     |

---

## Stack

| Capa        | Tecnología                          |
|-------------|-------------------------------------|
| Frontend    | Next.js 15, React 19, TS, Tailwind  |
| Backend     | FastAPI, SQLAlchemy 2               |
| BD          | PostgreSQL 15+                      |
| PDF         | pdfplumber + PyMuPDF                |
| NLP         | regex + spaCy (Sprint 2)            |
| IA          | OpenAI (Sprint 3+)                  |
