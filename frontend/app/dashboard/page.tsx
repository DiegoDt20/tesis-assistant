
"use client";

import { useEffect, useState } from "react";
import { apiFetch, getToken, removeToken } from "@/services/api";

interface Seccion {
  id: string;
  titulo: string;
  obligatoria: boolean;
  orden: number;
  hijos: Seccion[];
}

interface Plantilla {
  id: string;
  titulo: string;
  secciones: Seccion[];
  fecha_creacion: string;
}

interface Proyecto {
  id: string;
  titulo: string;
  estado: string;
  plantilla_id: string;
  respuestas: Record<string, string>;
  fecha_creacion: string;
}

export default function DashboardPage() {
  const [plantillas, setPlantillas] = useState<Plantilla[]>([]);
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    cargarDatos();
  }, []);

  async function cargarDatos() {
    try {
      const [p, pr] = await Promise.all([
        apiFetch<Plantilla[]>("/api/v1/plantillas/"),
        apiFetch<Proyecto[]>("/api/v1/proyectos/"),
      ]);
      setPlantillas(p);
      setProyectos(pr);
    } catch (err) {
      setError("Error al cargar los datos.");
    } finally {
      setCargando(false);
    }
  }

  function cerrarSesion() {
    removeToken();
    window.location.href = "/login";
  }

  if (cargando) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">Asistente de Tesis</h1>
          <button onClick={cerrarSesion} className="text-sm text-gray-500 hover:text-red-600">
            Cerrar sesión
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded mb-6 text-sm">{error}</div>
        )}

        <section className="mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-800">Mis Plantillas</h2>
            <a href="/upload" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
              + Nueva plantilla
            </a>
          </div>

          {plantillas.length === 0 ? (
            <div className="bg-white rounded-lg p-8 text-center text-gray-500 border">
              No tenés plantillas todavía.{" "}
              <a href="/upload" className="text-blue-600 hover:underline">Subí un PDF</a>{" "}
              para crear una.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {plantillas.map((p) => (
                <div key={p.id} className="bg-white rounded-lg p-5 border shadow-sm">
                  <h3 className="font-semibold text-gray-800 mb-2">{p.titulo}</h3>
                  <p className="text-sm text-gray-500 mb-3">{p.secciones.length} secciones</p>
                  <p className="text-xs text-gray-400">{new Date(p.fecha_creacion).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        <section>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-800">Mis Proyectos</h2>
          </div>

          {proyectos.length === 0 ? (
            <div className="bg-white rounded-lg p-8 text-center text-gray-500 border">
              No tenés proyectos todavía.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {proyectos.map((p) => (
                <div key={p.id} className="bg-white rounded-lg p-5 border shadow-sm">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-800">{p.titulo}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      p.estado === "completado" ? "bg-green-100 text-green-700"
                      : p.estado === "en_progreso" ? "bg-yellow-100 text-yellow-700"
                      : "bg-gray-100 text-gray-600"
                    }`}>
                      {p.estado}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 mb-3">{Object.keys(p.respuestas).length} respuestas completadas</p>
                  <p className="text-xs text-gray-400">{new Date(p.fecha_creacion).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}