import unittest

from sistema_escolar.mcp_client import MCPDemoClient, MCPError


class FakeMCPClient(MCPDemoClient):
    def __init__(self, responses):
        super().__init__(endpoint="http://fake-mcp")
        self.responses = list(responses)
        self.calls = []

    def _post(self, payload, session_id=None):
        self.calls.append((payload, session_id))
        if not self.responses:
            raise AssertionError("Sem resposta fake configurada")
        return self.responses.pop(0)


class MCPClientTests(unittest.TestCase):
    def test_cadastrar_aluno_retorna_structured_content(self):
        client = FakeMCPClient(
            responses=[
                ({"result": {"ok": True}}, "sessao-1"),
                ({}, "sessao-1"),
                (
                    {
                        "result": {
                            "structuredContent": {
                                "matricula": "001",
                                "nome": "Ana",
                                "status": "cadastrado",
                            }
                        }
                    },
                    None,
                ),
            ]
        )

        result = client.cadastrar_aluno("001", "Ana")

        self.assertEqual(result.get("structuredContent", {}).get("status"), "cadastrado")
        self.assertEqual(client.calls[2][0]["method"], "tools/call")
        self.assertEqual(client.calls[2][0]["params"]["name"], "cadastrar_aluno")

    def test_call_tool_com_erro_jsonrpc_levanta_mcperror(self):
        client = FakeMCPClient(
            responses=[
                ({"result": {"ok": True}}, "sessao-1"),
                ({}, "sessao-1"),
                ({"error": {"message": "tool indisponivel"}}, None),
            ]
        )

        with self.assertRaises(MCPError):
            client.call_tool("cadastrar_aluno", {"matricula": "001", "nome": "Ana"})


if __name__ == "__main__":
    unittest.main()