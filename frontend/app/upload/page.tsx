"use client";

import { useState } from "react";
import { uploadDocumento } from "@/services/documentos";
import { apiFetch } from "@/services/api";
import type { UploadResponse } from "@/types/documento";
import StructureList from "@/components/analysis/StructureList";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [creandoPlantilla, setCreandoPlantilla] = useState(false);
  const [plantillaCreada, setPlantillaCreada] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setPlantillaCreada(false);
    try {
      const data = await uploadDocumento(file);
      setResult(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCrearPlantilla() {
    if (!result) return;
    setCreandoPlantilla(true);
    setError(null);
    try {
      await apiFetch("/api/v1/plantillas/desde-documento", {
        method: "POST",
        body: JSON.stringify({
          documento_id: result.documento.id,
          titulo: result.documento.nombre.replace(".pdf", ""),
        }),
      });
      setPlantillaCreada(true);
      // Redirigir al dashboard después de 1.5 segundos
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1500);
    } catch (err) {
      setError("No se pudo crear la plantilla.");
    } finally {
      setCreandoPlantilla(false);
    }
  }

  return (
    <section className="max-w-3xl mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Subir Documento</h2>

      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl border p-6 space-y-4 shadow-sm"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Seleccioná tu guía de tesis en PDF
          </label>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <button
          type="submit"
          disabled={!file || loading}
          className="rounded-lg bg-blue-600 px-5 py-2 text-white disabled:opacity-50 hover:bg-blue-700"
        >
          {loading ? "Analizando..." : "Analizar PDF"}
        </button>

        {error && <p className="text-red-600 text-sm">{error}</p>}
      </form>

      {result && (
        <div className="mt-8">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold">
              Estructura detectada — {result.documento.nombre}
            </h3>
            {!plantillaCreada ? (
              <button
                onClick={handleCrearPlantilla}
                disabled={creandoPlantilla}
                className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700 disabled:opacity-50"
              >
                {creandoPlantilla ? "Creando..." : "✓ Crear plantilla"}
              </button>
            ) : (
              <span className="text-green-600 font-medium text-sm">
                ✓ Plantilla creada — redirigiendo...
              </span>
            )}
          </div>

          <StructureList nodos={result.estructura} />
        </div>
      )}
    </section>
  );
}