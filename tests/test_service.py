import tempfile
import unittest
from pathlib import Path

from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


class SistemaEscolarTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "alunos.json"
        self.sistema = SistemaEscolar(AlunoRepository(str(db_path)))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cadastra_aluno_com_sucesso(self) -> None:
        self.sistema.cadastrar_aluno("001", "Ana")

        alunos = self.sistema.listar_alunos()
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0].nome, "Ana")

    def test_nao_permite_matricula_duplicada(self) -> None:
        self.sistema.cadastrar_aluno("001", "Ana")

        with self.assertRaises(ValueError):
            self.sistema.cadastrar_aluno("001", "Bruno")

    def test_lanca_nota_e_calcula_media(self) -> None:
        self.sistema.cadastrar_aluno("001", "Ana")
        self.sistema.lancar_nota("001", 8)
        self.sistema.lancar_nota("001", 6)

        aluno = self.sistema.buscar_aluno("001")
        self.assertEqual(aluno.media, 7.0)
        self.assertEqual(aluno.situacao, "Aprovado")


if __name__ == "__main__":
    unittest.main()
