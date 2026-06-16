import tempfile
import unittest
from pathlib import Path

from sistema_escolar.microservices.notas_service import create_app


class NotasServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "notas_service.json"
        self.app = create_app(
            db_path=str(db_path),
            aluno_checker=lambda matricula: matricula == "001",
        )
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_lanca_nota_com_sucesso(self) -> None:
        response = self.client.post("/notas", json={"matricula": "001", "nota": 8})

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["matricula"], "001")
        self.assertEqual(payload["media"], 8.0)
        self.assertEqual(payload["situacao"], "Aprovado")

    def test_rejeita_nota_fora_da_faixa(self) -> None:
        response = self.client.post("/notas", json={"matricula": "001", "nota": 11})

        self.assertEqual(response.status_code, 400)
        self.assertIn("entre 0 e 10", response.get_json()["error"])

    def test_rejeita_aluno_inexistente(self) -> None:
        response = self.client.post("/notas", json={"matricula": "999", "nota": 7})

        self.assertEqual(response.status_code, 404)
        self.assertIn("Aluno nao encontrado", response.get_json()["error"])

    def test_consulta_notas_media_e_situacao(self) -> None:
        self.client.post("/notas", json={"matricula": "001", "nota": 5})
        self.client.post("/notas", json={"matricula": "001", "nota": 7})

        response = self.client.get("/notas/001")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["notas"], [5.0, 7.0])
        self.assertEqual(payload["media"], 6.0)
        self.assertEqual(payload["situacao"], "Aprovado")


if __name__ == "__main__":
    unittest.main()
