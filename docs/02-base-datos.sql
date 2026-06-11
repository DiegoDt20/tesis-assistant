-- =====================================================
-- Tesis Assistant — Esquema PostgreSQL (v1.0)
-- Sprint 1: usuarios, documentos, estructuras
-- =====================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ---------- USUARIOS ----------
CREATE TABLE usuarios (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre          VARCHAR(120)        NOT NULL,
    correo          VARCHAR(160) UNIQUE NOT NULL,
    password_hash   VARCHAR(255)        NOT NULL,
    rol             VARCHAR(20)         NOT NULL DEFAULT 'estudiante',
    activo          BOOLEAN             NOT NULL DEFAULT TRUE,
    fecha_creacion  TIMESTAMPTZ         NOT NULL DEFAULT NOW(),
    fecha_actualiz  TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_usuarios_correo ON usuarios(correo);

-- ---------- DOCUMENTOS ----------
CREATE TABLE documentos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre          VARCHAR(255)  NOT NULL,
    tipo            VARCHAR(30)   NOT NULL CHECK (tipo IN ('guia','tesis_modelo','borrador','final')),
    ruta_archivo    TEXT          NOT NULL,
    tamanio_bytes   BIGINT,
    paginas         INT,
    estado          VARCHAR(20)   NOT NULL DEFAULT 'subido'
                    CHECK (estado IN ('subido','procesando','analizado','error')),
    fecha_subida    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documentos_usuario ON documentos(usuario_id);
CREATE INDEX idx_documentos_estado  ON documentos(estado);

-- ---------- ESTRUCTURAS ----------
CREATE TABLE estructuras (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    documento_id    UUID NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
    parent_id       UUID REFERENCES estructuras(id) ON DELETE CASCADE,
    titulo          VARCHAR(300) NOT NULL,
    jerarquia       INT          NOT NULL DEFAULT 1,
    orden           INT          NOT NULL,
    contenido       TEXT,
    pagina_inicio   INT,
    fecha_creacion  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_estructuras_documento ON estructuras(documento_id);
CREATE INDEX idx_estructuras_parent    ON estructuras(parent_id);

-- ---------- PLANTILLAS (Sprint 2) ----------
CREATE TABLE plantillas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    documento_id    UUID REFERENCES documentos(id) ON DELETE SET NULL,
    titulo          VARCHAR(200) NOT NULL,
    secciones_json  JSONB        NOT NULL,
    fecha_creacion  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_plantillas_usuario ON plantillas(usuario_id);

-- ---------- TRIGGER auto-update ----------
CREATE OR REPLACE FUNCTION trg_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualiz = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION trg_set_updated_at();
