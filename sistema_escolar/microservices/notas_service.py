from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

from flask import Flask, jsonify, request


class NotaRepository:
    def __init__(self, db_path: str = "dados/notas_service.json") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def carregar(self) -> dict[str, list[float]]:
        if not self.db_path.exists():
            return {}

        raw = json.loads(self.db_path.read_text(encoding="utf-8"))
        result: dict[str, list[float]] = {}
        for matricula, notas in raw.items():
            if not isinstance(notas, list):
                continue
            result[str(matricula)] = [float(nota) for nota in notas]
        return result

    def salvar(self, notas_por_aluno: dict[str, list[float]]) -> None:
        self.db_path.write_text(
            json.dumps(notas_por_aluno, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def media(notas: list[float]) -> float:
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), 2)


def situacao(media_final: float) -> str:
    return "Aprovado" if media_final >= 6 else "Reprovado"


def default_aluno_checker(base_url: str, timeout: float = 3.0) -> Callable[[str], bool]:
    base = base_url.rstrip("/")

    def _checker(matricula: str) -> bool:
        url = f"{base}/alunos/{matricula}"
        request_obj = urllib.request.Request(url=url, method="GET")
        try:
            with urllib.request.urlopen(request_obj, timeout=timeout) as response:
                return response.status == 200
        except urllib.error.HTTPError:
            return False
        except urllib.error.URLError:
            return False

    return _checker


def create_app(
    db_path: str = "dados/notas_service.json",
    alunos_service_url: str | None = None,
    aluno_checker: Callable[[str], bool] | None = None,
) -> Flask:
    app = Flask(__name__)
    repository = NotaRepository(db_path)
    notas_por_aluno = repository.carregar()

    if alunos_service_url is None:
        alunos_service_url = os.getenv("ALUNOS_SERVICE_URL", "http://127.0.0.1:8002")
    checker = aluno_checker or default_aluno_checker(alunos_service_url)

    def sincronizar() -> None:
        nonlocal notas_por_aluno
        notas_por_aluno = repository.carregar()

    @app.get("/health")
    def health() -> tuple[dict, int]:
        return {"status": "ok", "service": "notas"}, 200

    @app.post("/notas")
    def lancar_nota():
        nonlocal notas_por_aluno

        payload = request.get_json(silent=True) or {}
        matricula = str(payload.get("matricula", "")).strip()
        if not matricula:
            return {"error": "A matricula nao pode ser vazia."}, 400

        try:
            nota = float(payload.get("nota"))
        except (TypeError, ValueError):
            return {"error": "A nota deve ser numerica."}, 400

        if nota < 0 or nota > 10:
            return {"error": "A nota deve estar entre 0 e 10."}, 400

        if not checker(matricula):
            return {"error": "Aluno nao encontrado no Alunos Service."}, 404

        sincronizar()
        notas_por_aluno.setdefault(matricula, []).append(nota)
        repository.salvar(notas_por_aluno)

        notas = notas_por_aluno[matricula]
        media_final = media(notas)
        return jsonify(
            {
                "matricula": matricula,
                "nota": nota,
                "media": media_final,
                "situacao": situacao(media_final),
            }
        ), 201

    @app.get("/notas/<matricula>")
    def consultar_notas(matricula: str):
        sincronizar()
        notas = notas_por_aluno.get(matricula)
        if notas is None:
            return {"error": "Notas nao encontradas para a matricula."}, 404

        media_final = media(notas)
        return {
            "matricula": matricula,
            "notas": notas,
            "media": media_final,
            "situacao": situacao(media_final),
        }, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8003, debug=True)
