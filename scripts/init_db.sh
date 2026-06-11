#!/usr/bin/env bash
# Inicializa la base de datos local para desarrollo.
set -euo pipefail

DB_NAME="${DB_NAME:-tesis_assistant}"
DB_USER="${DB_USER:-postgres}"

echo "==> Creando base de datos $DB_NAME"
createdb -U "$DB_USER" "$DB_NAME" || echo "(ya existe)"

echo "==> Aplicando esquema"
psql -U "$DB_USER" -d "$DB_NAME" -f docs/02-base-datos.sql

echo "==> Insertando usuario demo"
psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
INSERT INTO usuarios (id, nombre, correo, password_hash)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Demo',
    'demo@tesis.local',
    'demo'
) ON CONFLICT (id) DO NOTHING;
SQL

echo "OK"
