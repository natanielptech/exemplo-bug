import Link from "next/link";
import { redirect } from "next/navigation";

import { getSession } from "@/lib/auth";
import { estatisticas, listarAlunos } from "@/lib/school-store";

type DashboardPageProps = {
  searchParams?: {
    success?: string;
    error?: string;
  };
};

export default async function DashboardPage({ searchParams }: DashboardPageProps) {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }

  const [students, stats] = await Promise.all([listarAlunos(), estatisticas()]);

  const message = searchParams?.error ?? searchParams?.success ?? null;
  const isError = Boolean(searchParams?.error);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Sistema escolar</p>
          <h1>Painel de alunos e notas</h1>
          <p className="subtitle">
            Login ativo como <strong>{session.username}</strong>. Cadastro, notas e consulta funcionam em uma unica interface.
          </p>
        </div>

        <form action="/api/logout" method="post">
          <button type="submit" className="secondary-button">
            Sair
          </button>
        </form>
      </header>

      {message ? <div className={`notice ${isError ? "notice-error" : "notice-success"}`}>{message}</div> : null}

      <section className="stats-grid">
        <article className="stat-card">
          <span>Total</span>
          <strong>{stats.totalAlunos}</strong>
        </article>
        <article className="stat-card">
          <span>Aprovados</span>
          <strong>{stats.aprovados}</strong>
        </article>
        <article className="stat-card">
          <span>Reprovados</span>
          <strong>{stats.reprovados}</strong>
        </article>
        <article className="stat-card">
          <span>Media geral</span>
          <strong>{stats.mediaGeral.toFixed(2)}</strong>
        </article>
      </section>

      <section className="panel-grid">
        <article className="panel">
          <div className="panel-title">
            <p className="eyebrow">Cadastro</p>
            <h2>Novo aluno</h2>
          </div>

          <form action="/api/students" method="post" className="stack-form">
            <label>
              Matricula
              <input name="matricula" type="text" placeholder="001" required />
            </label>
            <label>
              Nome
              <input name="nome" type="text" placeholder="Ana Silva" required />
            </label>
            <button type="submit" className="primary-button">
              Cadastrar aluno
            </button>
          </form>
        </article>

        <article className="panel">
          <div className="panel-title">
            <p className="eyebrow">Notas</p>
            <h2>Lancar nota</h2>
          </div>

          <form action="/api/students/grades" method="post" className="stack-form">
            <label>
              Matricula
              <input name="matricula" type="text" placeholder="001" required />
            </label>
            <label>
              Nota
              <input name="nota" type="number" step="0.1" min="0" max="10" placeholder="8" required />
            </label>
            <button type="submit" className="primary-button">
              Registrar nota
            </button>
          </form>
        </article>
      </section>

      <section className="panel">
        <div className="panel-title">
          <p className="eyebrow">Alunos</p>
          <h2>Lista cadastrada</h2>
        </div>

        {students.length ? (
          <div className="student-grid">
            {students.map((student) => (
              <article key={student.matricula} className="student-card">
                <div className="student-card-head">
                  <div>
                    <span className="student-name">{student.nome}</span>
                    <p className="student-meta">Matricula {student.matricula}</p>
                  </div>
                  <span className={`status-pill ${student.situacao === "Aprovado" ? "status-ok" : "status-warn"}`}>
                    {student.situacao}
                  </span>
                </div>

                <div className="student-metrics">
                  <div>
                    <span>Media</span>
                    <strong>{student.media.toFixed(2)}</strong>
                  </div>
                  <div>
                    <span>Notas</span>
                    <strong>{student.notas.length}</strong>
                  </div>
                </div>

                <div className="card-actions">
                  <Link className="text-link" href={`/alunos/${student.matricula}`}>
                    Ver detalhe
                  </Link>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <p className="empty-state">Nenhum aluno cadastrado ainda. Use o formulario acima para comecar.</p>
        )}
      </section>
    </main>
  );
}
