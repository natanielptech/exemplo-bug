import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { getSession } from "@/lib/auth";
import { buscarAluno } from "@/lib/school-store";

type StudentPageProps = {
  params: Promise<{ matricula: string }> | { matricula: string };
  searchParams?: {
    success?: string;
    error?: string;
  };
};

export default async function StudentPage({ params, searchParams }: StudentPageProps) {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }

  const resolvedParams = await params;

  try {
    const student = await buscarAluno(resolvedParams.matricula);
    const notice = searchParams?.error ?? searchParams?.success ?? null;

    return (
      <main className="app-shell">
        <header className="topbar compact">
          <div>
            <p className="eyebrow">Detalhe do aluno</p>
            <h1>{student.nome}</h1>
            <p className="subtitle">Matricula {student.matricula}</p>
          </div>

          <Link href="/dashboard" className="secondary-button link-button">
            Voltar
          </Link>
        </header>

        {notice ? <div className="notice notice-success">{notice}</div> : null}

        <section className="panel-grid detail-grid">
          <article className="panel">
            <div className="panel-title">
              <p className="eyebrow">Resumo</p>
              <h2>Informacoes</h2>
            </div>

            <div className="detail-stack">
              <div>
                <span>Media</span>
                <strong>{student.media.toFixed(2)}</strong>
              </div>
              <div>
                <span>Situacao</span>
                <strong>{student.situacao}</strong>
              </div>
              <div>
                <span>Total de notas</span>
                <strong>{student.notas.length}</strong>
              </div>
            </div>

            <form action={`/api/students/${student.matricula}/grades`} method="post" className="stack-form compact-form">
              <label>
                Nova nota
                <input name="nota" type="number" min="0" max="10" step="0.1" placeholder="9" required />
              </label>
              <button type="submit" className="primary-button">
                Registrar nota
              </button>
            </form>
          </article>

          <article className="panel">
            <div className="panel-title">
              <p className="eyebrow">Historico</p>
              <h2>Notas lancadas</h2>
            </div>

            {student.notas.length ? (
              <ul className="grade-list">
                {student.notas.map((nota, index) => (
                  <li key={`${student.matricula}-${index}`}>
                    <span>Nota {index + 1}</span>
                    <strong>{nota.toFixed(1)}</strong>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="empty-state">Nenhuma nota lancada.</p>
            )}
          </article>
        </section>
      </main>
    );
  } catch {
    notFound();
  }
}
