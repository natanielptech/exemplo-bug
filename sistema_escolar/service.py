from typing import Dict, List

from sistema_escolar.models import Aluno
from sistema_escolar.repository import AlunoRepository


class SistemaEscolar:
    def __init__(self, repository: AlunoRepository) -> None:
        self.repository = repository
        self.alunos: Dict[str, Aluno] = self.repository.carregar()

    def cadastrar_aluno(self, matricula: str, nome: str) -> None:
        if not matricula.strip():
            raise ValueError("A matricula nao pode ser vazia.")
        if not nome.strip():
            raise ValueError("O nome nao pode ser vazio.")
        if matricula in self.alunos:
            raise ValueError("Ja existe um aluno com essa matricula.")

        self.alunos[matricula] = Aluno(matricula=matricula, nome=nome)
        self.repository.salvar(self.alunos)

    def lancar_nota(self, matricula: str, nota: float) -> None:
        aluno = self.alunos.get(matricula)
        if not aluno:
            raise ValueError("Aluno nao encontrado.")

        aluno.adicionar_nota(nota)
        self.repository.salvar(self.alunos)

    def listar_alunos(self) -> List[Aluno]:
        return sorted(self.alunos.values(), key=lambda a: a.nome.lower())

    def buscar_aluno(self, matricula: str) -> Aluno:
        aluno = self.alunos.get(matricula)
        if not aluno:
            raise ValueError("Aluno nao encontrado.")
        return aluno
