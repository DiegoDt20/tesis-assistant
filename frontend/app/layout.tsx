import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tesis Assistant",
  description: "Asistente inteligente para tesis universitarias.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <header className="border-b bg-white">
          <div className="mx-auto max-w-5xl px-6 py-4 flex items-center justify-between">
            <h1 className="text-lg font-semibold text-brand">Tesis Assistant</h1>
            <nav className="text-sm text-slate-600 space-x-4">
              <a href="/">Inicio</a>
              <a href="/upload">Subir</a>
              <a href="/dashboard">Mis documentos</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
      </body>
    </html>
  );
}
