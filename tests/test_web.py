import tempfile
import unittest
from pathlib import Path

from sistema_escolar.mcp_client import MCPError, MCPTool
from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar
from sistema_escolar.web import create_app


class FakeMCPClient:
    def __init__(self, should_fail: bool = False) -> None:
        self.endpoint = "https://mcp.exemplo.publico/mcp"
        self.should_fail = should_fail

    def list_tools(self, limit: int = 8):
        if self.should_fail:
            raise MCPError("Erro de conexao no servidor MCP de teste.")
        return [
            MCPTool(name="search_docs", description="Busca documentacao"),
            MCPTool(name="list_examples", description="Lista exemplos"),
        ][:limit]


class SistemaEscolarWebTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "alunos.json"
        self.app = create_app(str(db_path), mcp_client=FakeMCPClient())
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def login(self) -> None:
        self.client.post(
            "/login",
            data={"usuario": "nataniel", "senha": "123"},
            follow_redirects=False,
        )

    def test_rota_index_redireciona_para_login_sem_sessao(self) -> None:
        response = self.client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_login_com_credenciais_invalidas(self) -> None:
        response = self.client.post(
            "/login",
            data={"usuario": "invalido", "senha": "errada"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário ou senha inválidos.".encode("utf-8"), response.data)

    def test_index_renderiza_com_usuario_logado(self) -> None:
        self.login()

        response = self.client.get("/", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sistema Escolar".encode("utf-8"), response.data)

    def test_fluxo_cadastro_e_lancamento_de_nota(self) -> None:
        self.login()

        response_cadastro = self.client.post(
            "/",
            data={"acao": "cadastrar", "matricula": "001", "nome": "Ana"},
            follow_redirects=True,
        )
        self.assertEqual(response_cadastro.status_code, 200)
        self.assertIn("Aluno cadastrado com sucesso.".encode("utf-8"), response_cadastro.data)

        response_nota = self.client.post(
            "/",
            data={"acao": "nota", "matricula_nota": "001", "nota": "8"},
            follow_redirects=True,
        )
        self.assertEqual(response_nota.status_code, 200)
        self.assertIn("Nota registrada com sucesso.".encode("utf-8"), response_nota.data)

    def test_index_reflete_cadastro_externo_no_mesmo_json(self) -> None:
        self.login()

        sistema_externo = SistemaEscolar(AlunoRepository(str(Path(self.temp_dir.name) / "alunos.json")))
        sistema_externo.cadastrar_aluno("9900", "Aluno Externo")

        response = self.client.get("/", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Aluno Externo".encode("utf-8"), response.data)

    def test_acao_invalida_exibe_erro(self) -> None:
        self.login()

        response = self.client.post(
            "/",
            data={"acao": "desconhecida"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Acao invalida.".encode("utf-8"), response.data)

    def test_logout_remove_sessao_e_bloqueia_index(self) -> None:
        self.login()

        self.client.get("/logout", follow_redirects=False)
        response = self.client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_mcp_demo_redireciona_para_login_sem_sessao(self) -> None:
        response = self.client.get("/mcp-demo", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_mcp_demo_exibe_lista_de_ferramentas(self) -> None:
        self.login()

        response = self.client.get("/mcp-demo", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_docs".encode("utf-8"), response.data)
        self.assertIn("list_examples".encode("utf-8"), response.data)

    def test_mcp_demo_exibe_erro_quando_cliente_falha(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        try:
            db_path = Path(temp_dir.name) / "alunos.json"
            app = create_app(str(db_path), mcp_client=FakeMCPClient(should_fail=True))
            app.config["TESTING"] = True
            client = app.test_client()

            client.post(
                "/login",
                data={"usuario": "nataniel", "senha": "123"},
                follow_redirects=False,
            )

            response = client.get("/mcp-demo", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "Erro de conexao no servidor MCP de teste.".encode("utf-8"),
                response.data,
            )
        finally:
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()