"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/services/api";

interface Plantilla {
  id: string;
  titulo: string;
  secciones: { id: string; titulo: string }[];
}

export default function NuevoProyectoPage() {
  const [plantillas, setPlantillas] = useState<Plantilla[]>([]);
  const [titulo, setTitulo] = useState("");
  const [plantillaId, setPlantillaId] = useState("");
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    cargarPlantillas();
  }, []);

  async function cargarPlantillas() {
    try {
      const data = await apiFetch<Plantilla[]>("/api/v1/plantillas/");
      setPlantillas(data);
      if (data.length > 0) setPlantillaId(data[0].id);
    } catch {
      setError("Error al cargar las plantillas.");
    } finally {
      setCargando(false);
    }
  }

  async function handleCrear(e: React.FormEvent) {
    e.preventDefault();
    if (!titulo || !plantillaId) return;
    setGuardando(true);
    setError("");

    try {
      await apiFetch("/api/v1/proyectos/", {
        method: "POST",
        body: JSON.stringify({
          titulo,
          plantilla_id: plantillaId,
        }),
      });
      window.location.href = "/dashboard";
    } catch {
      setError("No se pudo crear el proyecto.");
    } finally {
      setGuardando(false);
    }
  }

  if (cargando) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Cargando plantillas...</p>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Nuevo Proyecto</h2>

      {plantillas.length === 0 ? (
        <div className="bg-white rounded-lg p-8 text-center text-gray-500 border">
          No tenés plantillas disponibles.{" "}
          <a href="/upload" className="text-blue-600 hover:underline">
            Subí un PDF primero
          </a>.
        </div>
      ) : (
        <form
          onSubmit={handleCrear}
          className="bg-white rounded-xl border p-6 space-y-5 shadow-sm"
        >
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Título del proyecto
            </label>
            <input
              type="text"
              value={titulo}
              onChange={(e) => setTitulo(e.target.value)}
              required
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ej: Mi investigación sobre educación virtual"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Plantilla base
            </label>
            <select
              value={plantillaId}
              onChange={(e) => setPlantillaId(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {plantillas.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.titulo} ({p.secciones.length} secciones)
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            disabled={guardando || !titulo}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {guardando ? "Creando..." : "Crear proyecto"}
          </button>
        </form>
      )}
    </div>
  );
}