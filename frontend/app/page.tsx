import Link from "next/link";

export default function HomePage() {
  return (
    <section className="text-center py-16">
      <h2 className="text-3xl font-bold text-slate-800">
        Analiza la estructura de tu guía de tesis automáticamente
      </h2>
      <p className="mt-4 text-slate-600 max-w-2xl mx-auto">
        Sube un PDF y el sistema detectará capítulos, secciones y la jerarquía documental.
      </p>
      <Link
        href="/upload"
        className="inline-block mt-8 rounded-lg bg-brand px-6 py-3 text-white hover:bg-brand-dark"
      >
        Subir Documento
      </Link>
    </section>
  );
}
