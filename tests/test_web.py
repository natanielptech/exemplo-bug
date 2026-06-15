import tempfile
import unittest
from pathlib import Path

from sistema_escolar.web import create_app


class SistemaEscolarWebTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "alunos.json"
        self.app = create_app(str(db_path))
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_index_renderiza(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sistema Escolar", response.data)


if __name__ == "__main__":
    unittest.main()