"use client";

import { useState } from "react";
import { uploadDocumento } from "@/services/documentos";
import type { UploadResponse } from "@/types/documento";
import StructureList from "@/components/analysis/StructureList";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResponse | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await uploadDocumento(file);
      setResult(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2 className="text-2xl font-bold mb-4">Subir Documento</h2>

      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl border p-6 space-y-4 shadow-sm"
      >
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="block w-full text-sm"
        />
        <button
          type="submit"
          disabled={!file || loading}
          className="rounded-lg bg-brand px-5 py-2 text-white disabled:opacity-50"
        >
          {loading ? "Analizando..." : "Analizar PDF"}
        </button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
      </form>

      {result && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-2">
            Estructura detectada — {result.documento.nombre}
          </h3>
          <StructureList nodos={result.estructura} />
        </div>
      )}
    </section>
  );
}
