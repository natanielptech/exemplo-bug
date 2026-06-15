from __future__ import annotations

from statistics import mean

from flask import Flask, flash, redirect, render_template, request, url_for

from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


def create_app(db_path: str = "dados/alunos.json") -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "sistema-escolar-desenvolvimento"

    sistema = SistemaEscolar(AlunoRepository(db_path))

    def montar_estatisticas() -> dict[str, float | int]:
        alunos = sistema.listar_alunos()
        total_alunos = len(alunos)
        aprovados = sum(1 for aluno in alunos if aluno.situacao == "Aprovado")
        media_geral = round(mean([aluno.media for aluno in alunos]), 2) if alunos else 0.0
        return {
            "total_alunos": total_alunos,
            "aprovados": aprovados,
            "reprovados": total_alunos - aprovados,
            "media_geral": media_geral,
        }

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
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
        estatisticas = montar_estatisticas()
        return render_template(
            "index.html",
            alunos=alunos,
            estatisticas=estatisticas,
        )

    @app.route("/alunos/<matricula>")
    def detalhe_aluno(matricula: str) -> str:
        try:
            aluno = sistema.buscar_aluno(matricula)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        return render_template("aluno.html", aluno=aluno)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)