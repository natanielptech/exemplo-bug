import json
import tempfile
import unittest
from pathlib import Path

from sistema_escolar.mcp_server import create_mcp_app
from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


class MCPServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "alunos.json"
        self.app = create_mcp_app(str(self.db_path))
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def post_jsonrpc(self, payload: dict) -> tuple[int, dict, dict]:
        response = self.client.post(
            "/mcp",
            data=json.dumps(payload),
            content_type="application/json",
        )
        body = response.get_json(silent=True) or {}
        return response.status_code, body, dict(response.headers)

    def test_initialize_retorna_session_id(self) -> None:
        status, body, headers = self.post_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "teste", "version": "1.0.0"},
                },
            }
        )

        self.assertEqual(status, 200)
        self.assertEqual(body.get("result", {}).get("serverInfo", {}).get("name"), "sistema-escolar-mcp")
        self.assertTrue(headers.get("MCP-Session-Id"))

    def test_tools_list_inclui_cadastrar_aluno(self) -> None:
        status, body, _ = self.post_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }
        )

        self.assertEqual(status, 200)
        tools = body.get("result", {}).get("tools", [])
        nomes = [tool.get("name") for tool in tools]
        self.assertIn("cadastrar_aluno", nomes)

    def test_tools_call_cadastra_aluno(self) -> None:
        status, body, _ = self.post_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "cadastrar_aluno",
                    "arguments": {
                        "matricula": "001",
                        "nome": "Ana",
                    },
                },
            }
        )

        self.assertEqual(status, 200)
        self.assertEqual(body.get("result", {}).get("structuredContent", {}).get("status"), "cadastrado")

        sistema = SistemaEscolar(AlunoRepository(str(self.db_path)))
        aluno = sistema.buscar_aluno("001")
        self.assertEqual(aluno.nome, "Ana")

    def test_tools_call_retorna_erro_de_negocio(self) -> None:
        primeiro_status, _, _ = self.post_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "cadastrar_aluno",
                    "arguments": {
                        "matricula": "001",
                        "nome": "Ana",
                    },
                },
            }
        )
        self.assertEqual(primeiro_status, 200)

        status, body, _ = self.post_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "cadastrar_aluno",
                    "arguments": {
                        "matricula": "001",
                        "nome": "Ana de novo",
                    },
                },
            }
        )

        self.assertEqual(status, 200)
        self.assertTrue(body.get("result", {}).get("isError"))


if __name__ == "__main__":
    unittest.main()