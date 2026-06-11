import { apiFetch } from "./api";
import type { UploadResponse } from "@/types/documento";

export async function uploadDocumento(
  file: File,
  tipo: string = "guia"
): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  return apiFetch<UploadResponse>(
    `/api/v1/documentos/upload?tipo=${encodeURIComponent(tipo)}`,
    { method: "POST", body: form }
  );
}
