from __future__ import annotations

from functools import wraps
from statistics import mean

from flask import Flask, flash, redirect, render_template, request, session, url_for

from sistema_escolar.mcp_client import MCPDemoClient, MCPError
from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


# Credenciais de demo em memória
VALID_CREDENTIALS = {
    "nataniel": "123"
}


def create_app(
    db_path: str = "dados/alunos.json",
    mcp_client: MCPDemoClient | None = None,
) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "sistema-escolar-desenvolvimento"

    sistema = SistemaEscolar(AlunoRepository(db_path))
    mcp_demo_client = mcp_client or MCPDemoClient.from_env()

    def sincronizar_com_arquivo() -> None:
        sistema.alunos = sistema.repository.carregar()

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "usuario" not in session:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function

    def montar_estatisticas(alunos) -> dict[str, float | int]:
        total_alunos = len(alunos)
        aprovados = sum(1 for aluno in alunos if aluno.situacao == "Aprovado")
        media_geral = round(mean([aluno.media for aluno in alunos]), 2) if alunos else 0.0
        return {
            "total_alunos": total_alunos,
            "aprovados": aprovados,
            "reprovados": total_alunos - aprovados,
            "media_geral": media_geral,
        }

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "").strip()

            if usuario in VALID_CREDENTIALS and VALID_CREDENTIALS[usuario] == senha:
                session["usuario"] = usuario
                flash(f"Bem-vindo, {usuario}!", "success")
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Usuário ou senha inválidos.")

        if "usuario" in session:
            return redirect(url_for("index"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("usuario", None)
        flash("Você foi desconectado.", "success")
        return redirect(url_for("login"))

    @app.route("/", methods=["GET", "POST"])
    @login_required
    def index() -> str:
        sincronizar_com_arquivo()

        if request.method == "POST":
            acao = request.form.get("acao", "")

            try:
                if acao == "cadastrar":
                    sistema.cadastrar_aluno(
                        request.form.get("matricula", "").strip(),
                        request.form.get("nome", "").strip(),
                    )
                    flash("Aluno cadastrado com sucesso.", "success")
                elif acao == "nota":
                    sistema.lancar_nota(
                        request.form.get("matricula_nota", "").strip(),
                        float(request.form.get("nota", "").strip()),
                    )
                    flash("Nota registrada com sucesso.", "success")
                else:
                    flash("Acao invalida.", "error")
            except ValueError as exc:
                flash(str(exc), "error")

            return redirect(url_for("index"))

        alunos = sistema.listar_alunos()
        estatisticas = montar_estatisticas(alunos)
        return render_template(
            "index.html",
            alunos=alunos,
            estatisticas=estatisticas,
        )

    @app.route("/alunos/<matricula>")
    @login_required
    def detalhe_aluno(matricula: str) -> str:
        sincronizar_com_arquivo()

        try:
            aluno = sistema.buscar_aluno(matricula)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        return render_template("aluno.html", aluno=aluno)

    @app.route("/mcp-demo")
    @login_required
    def mcp_demo() -> str:
        tools = []
        erro = None
        try:
            tools = mcp_demo_client.list_tools(limit=8)
        except MCPError as exc:
            erro = str(exc)

        return render_template(
            "mcp_demo.html",
            tools=tools,
            erro=erro,
            endpoint=mcp_demo_client.endpoint,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)