import type { EstructuraNode } from "@/types/documento";

interface Props {
  nodos: EstructuraNode[];
}

export default function StructureList({ nodos }: Props) {
  if (!nodos.length) {
    return <p className="text-slate-500">No se detectaron secciones.</p>;
  }
  return (
    <ul className="bg-white rounded-xl border divide-y">
      {nodos.map((n) => (
        <li
          key={n.orden}
          className="flex items-center justify-between px-4 py-2"
          style={{ paddingLeft: `${1 + (n.jerarquia - 1) * 1.5}rem` }}
        >
          <span className="text-slate-800">
            <span className="text-emerald-600 mr-2">✓</span>
            {n.titulo}
          </span>
          {n.pagina_inicio && (
            <span className="text-xs text-slate-400">p.{n.pagina_inicio}</span>
          )}
        </li>
      ))}
    </ul>
  );
}
