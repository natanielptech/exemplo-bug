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

    def test_nao_permite_matricula_vazia(self) -> None:
        with self.assertRaises(ValueError):
            self.sistema.cadastrar_aluno("   ", "Ana")

    def test_nao_permite_nome_vazio(self) -> None:
        with self.assertRaises(ValueError):
            self.sistema.cadastrar_aluno("001", "   ")

    def test_lanca_nota_e_calcula_media(self) -> None:
        self.sistema.cadastrar_aluno("001", "Ana")
        self.sistema.lancar_nota("001", 8)
        self.sistema.lancar_nota("001", 6)

        aluno = self.sistema.buscar_aluno("001")
        self.assertEqual(aluno.media, 7.0)
        self.assertEqual(aluno.situacao, "Aprovado")

    def test_lancar_nota_para_aluno_inexistente(self) -> None:
        with self.assertRaises(ValueError):
            self.sistema.lancar_nota("999", 8)

    def test_nao_permite_nota_fora_da_faixa(self) -> None:
        self.sistema.cadastrar_aluno("001", "Ana")

        with self.assertRaises(ValueError):
            self.sistema.lancar_nota("001", 11)

    def test_buscar_aluno_inexistente(self) -> None:
        with self.assertRaises(ValueError):
            self.sistema.buscar_aluno("999")

    def test_lista_alunos_em_ordem_alfabetica_sem_diferenciar_maiusculas(self) -> None:
        self.sistema.cadastrar_aluno("001", "zeca")
        self.sistema.cadastrar_aluno("002", "Ana")
        self.sistema.cadastrar_aluno("003", "bruno")

        alunos = self.sistema.listar_alunos()

        self.assertEqual([aluno.nome for aluno in alunos], ["Ana", "bruno", "zeca"])


if __name__ == "__main__":
    unittest.main()
