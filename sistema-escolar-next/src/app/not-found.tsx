import Link from "next/link";

export default function NotFound() {
  return (
    <main className="app-shell centered-shell">
      <section className="panel centered-panel">
        <p className="eyebrow">404</p>
        <h1>Aluno nao encontrado</h1>
        <p className="subtitle">A pagina solicitada nao existe ou a matricula informada nao foi localizada.</p>
        <Link href="/dashboard" className="primary-button link-button">
          Voltar ao painel
        </Link>
      </section>
    </main>
  );
}
