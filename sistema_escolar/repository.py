import json
from pathlib import Path
from typing import Dict

from sistema_escolar.models import Aluno


class AlunoRepository:
    def __init__(self, db_path: str = "dados/alunos.json") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def carregar(self) -> Dict[str, Aluno]:
        if not self.db_path.exists():
            return {}

        raw = json.loads(self.db_path.read_text(encoding="utf-8"))
        return {
            matricula: Aluno(
                matricula=matricula,
                nome=payload["nome"],
                notas=payload.get("notas", []),
            )
            for matricula, payload in raw.items()
        }

    def salvar(self, alunos: Dict[str, Aluno]) -> None:
        serializado = {
            matricula: {"nome": aluno.nome, "notas": aluno.notas}
            for matricula, aluno in alunos.items()
        }
        self.db_path.write_text(
            json.dumps(serializado, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
