import tempfile
import unittest
from pathlib import Path

from sistema_escolar.microservices.alunos_service import create_app


class AlunosServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "alunos_service.json"
        self.app = create_app(str(db_path))
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cadastra_aluno_com_sucesso(self) -> None:
        response = self.client.post("/alunos", json={"matricula": "001", "nome": "Ana"})

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["matricula"], "001")
        self.assertEqual(payload["nome"], "Ana")

    def test_rejeita_matricula_duplicada(self) -> None:
        self.client.post("/alunos", json={"matricula": "001", "nome": "Ana"})

        response = self.client.post("/alunos", json={"matricula": "001", "nome": "Bruno"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Ja existe", response.get_json()["error"])

    def test_lista_alunos_ordenados(self) -> None:
        self.client.post("/alunos", json={"matricula": "003", "nome": "zeca"})
        self.client.post("/alunos", json={"matricula": "001", "nome": "Ana"})
        self.client.post("/alunos", json={"matricula": "002", "nome": "bruno"})

        response = self.client.get("/alunos")

        self.assertEqual(response.status_code, 200)
        nomes = [item["nome"] for item in response.get_json()["items"]]
        self.assertEqual(nomes, ["Ana", "bruno", "zeca"])

    def test_busca_aluno_por_matricula(self) -> None:
        self.client.post("/alunos", json={"matricula": "001", "nome": "Ana"})

        response = self.client.get("/alunos/001")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["nome"], "Ana")


if __name__ == "__main__":
    unittest.main()
