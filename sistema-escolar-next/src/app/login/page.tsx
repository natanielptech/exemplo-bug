import { redirect } from "next/navigation";

import { getSession } from "@/lib/auth";

type LoginPageProps = {
  searchParams?: {
    error?: string;
  };
};

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const session = await getSession();
  if (session) {
    redirect("/dashboard");
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <div className="auth-badge">Sistema escolar</div>
        <h1>Login</h1>
        <p className="auth-copy">
          Acesse o painel para cadastrar alunos, lancar notas e acompanhar o rendimento.
        </p>

        {searchParams?.error ? <div className="notice notice-error">{searchParams.error}</div> : null}

        <form action="/api/login" method="post" className="auth-form">
          <label>
            Usuario
            <input name="usuario" type="text" placeholder="nataniel" required />
          </label>
          <label>
            Senha
            <input name="senha" type="password" placeholder="123" required />
          </label>
          <button type="submit" className="primary-button">
            Entrar
          </button>
        </form>

        <p className="auth-hint">Credenciais padrao: nataniel / 123</p>
      </section>
    </main>
  );
}
