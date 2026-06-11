export interface EstructuraNode {
  titulo: string;
  jerarquia: number;
  orden: number;
  pagina_inicio: number | null;
  hijos?: EstructuraNode[];
}

export interface Documento {
  id: string;
  nombre: string;
  tipo: string;
  estado: string;
  paginas: number | null;
  fecha_subida: string;
}

export interface UploadResponse {
  documento: Documento;
  estructura: EstructuraNode[];
}
