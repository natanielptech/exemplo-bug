from __future__ import annotations

import uuid
from typing import Any

from flask import Flask, Response, jsonify, request

from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


def create_mcp_app(db_path: str = "dados/alunos.json") -> Flask:
    app = Flask(__name__)
    sistema = SistemaEscolar(AlunoRepository(db_path))
    sessions: set[str] = set()

    def rpc_error(request_id: Any, code: int, message: str) -> tuple[Response, int]:
        return (
            jsonify(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": code,
                        "message": message,
                    },
                }
            ),
            200,
        )

    @app.post("/mcp")
    def mcp() -> Response | tuple[Response, int]:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return rpc_error(None, -32700, "JSON invalido.")

        request_id = payload.get("id")
        method = payload.get("method")
        params = payload.get("params") or {}

        if not isinstance(method, str):
            return rpc_error(request_id, -32600, "Requisicao JSON-RPC invalida.")

        if method == "initialize":
            session_id = str(uuid.uuid4())
            sessions.add(session_id)
            response = jsonify(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {
                                "listChanged": False,
                            }
                        },
                        "serverInfo": {
                            "name": "sistema-escolar-mcp",
                            "version": "1.0.0",
                        },
                    },
                }
            )
            response.headers["MCP-Session-Id"] = session_id
            return response

        if method == "notifications/initialized":
            return (Response(status=204), 204)

        if method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "cadastrar_aluno",
                        "description": "Cadastra um aluno no sistema escolar.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "matricula": {
                                    "type": "string",
                                    "description": "Matricula unica do aluno.",
                                },
                                "nome": {
                                    "type": "string",
                                    "description": "Nome completo do aluno.",
                                },
                            },
                            "required": ["matricula", "nome"],
                        },
                    }
                ]
            }
            return jsonify({"jsonrpc": "2.0", "id": request_id, "result": result})

        if method == "tools/call":
            if not isinstance(params, dict):
                return rpc_error(request_id, -32602, "Parametros invalidos.")

            tool_name = params.get("name")
            arguments = params.get("arguments") or {}

            if tool_name != "cadastrar_aluno":
                return rpc_error(request_id, -32601, "Tool nao encontrada.")

            if not isinstance(arguments, dict):
                return rpc_error(request_id, -32602, "Arguments invalidos.")

            matricula = str(arguments.get("matricula", "")).strip()
            nome = str(arguments.get("nome", "")).strip()

            try:
                sistema.cadastrar_aluno(matricula, nome)
            except ValueError as exc:
                return jsonify(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": str(exc),
                                }
                            ],
                            "isError": True,
                        },
                    }
                )

            return jsonify(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Aluno {nome} ({matricula}) cadastrado com sucesso.",
                            }
                        ],
                        "structuredContent": {
                            "matricula": matricula,
                            "nome": nome,
                            "status": "cadastrado",
                        },
                    },
                }
            )

        return rpc_error(request_id, -32601, "Metodo nao encontrado.")

    return app


app = create_mcp_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)