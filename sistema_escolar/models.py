from dataclasses import dataclass, field
from typing import List


@dataclass
class Aluno:
    matricula: str
    nome: str
    notas: List[float] = field(default_factory=list)

    def adicionar_nota(self, nota: float) -> None:
        if nota < 0 or nota > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        self.notas.append(nota)

    @property
    def media(self) -> float:
        if not self.notas:
            return 0.0
        return round(sum(self.notas) / len(self.notas), 2)

    @property
    def situacao(self) -> str:
        return "Aprovado" if self.media >= 6 else "Reprovado"
