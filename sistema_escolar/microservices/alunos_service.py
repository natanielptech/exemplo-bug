from __future__ import annotations

from flask import Flask, jsonify, request

from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


def _aluno_to_dict(aluno) -> dict:
    return {
        "matricula": aluno.matricula,
        "nome": aluno.nome,
    }


def create_app(db_path: str = "dados/alunos_service.json") -> Flask:
    app = Flask(__name__)
    sistema = SistemaEscolar(AlunoRepository(db_path))

    def sincronizar() -> None:
        sistema.alunos = sistema.repository.carregar()

    @app.get("/health")
    def health() -> tuple[dict, int]:
        return {"status": "ok", "service": "alunos"}, 200

    @app.get("/alunos")
    def listar_alunos() -> tuple[dict, int]:
        sincronizar()
        alunos = [_aluno_to_dict(aluno) for aluno in sistema.listar_alunos()]
        return {"items": alunos}, 200

    @app.get("/alunos/<matricula>")
    def buscar_aluno(matricula: str):
        sincronizar()
        try:
            aluno = sistema.buscar_aluno(matricula)
        except ValueError as exc:
            return {"error": str(exc)}, 404
        return _aluno_to_dict(aluno), 200

    @app.post("/alunos")
    def cadastrar_aluno():
        payload = request.get_json(silent=True) or {}
        matricula = str(payload.get("matricula", "")).strip()
        nome = str(payload.get("nome", "")).strip()

        try:
            sistema.cadastrar_aluno(matricula, nome)
        except ValueError as exc:
            return {"error": str(exc)}, 400

        aluno = sistema.buscar_aluno(matricula)
        return jsonify(_aluno_to_dict(aluno)), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8002, debug=True)
