from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class MCPError(RuntimeError):
    """Erro de comunicação com servidor MCP."""


@dataclass
class MCPTool:
    name: str
    description: str | None = None


class MCPDemoClient:
    def __init__(self, endpoint: str, timeout: float = 8.0) -> None:
        self.endpoint = endpoint
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "MCPDemoClient":
        endpoint = os.getenv("MCP_DEMO_URL", "https://mcp.deepwiki.com/mcp")
        return cls(endpoint=endpoint)

    @staticmethod
    def _decode_response(raw: str) -> dict[str, Any]:
        payload = raw.strip()
        if not payload:
            return {}

        if payload.startswith("event:"):
            for line in payload.splitlines():
                if line.startswith("data:"):
                    payload = line[5:].strip()
                    break

        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise MCPError("Resposta invalida do servidor MCP.") from exc

        if isinstance(parsed, list):
            if not parsed:
                return {}
            first = parsed[0]
            if isinstance(first, dict):
                return first
            return {}

        if not isinstance(parsed, dict):
            return {}

        return parsed

    def _post(self, payload: dict[str, Any], session_id: str | None = None) -> tuple[dict[str, Any], str | None]:
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if session_id:
            headers["MCP-Session-Id"] = session_id

        request = urllib.request.Request(
            url=self.endpoint,
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                new_session_id = response.headers.get("MCP-Session-Id")
        except urllib.error.HTTPError as exc:
            raise MCPError(f"Servidor MCP retornou HTTP {exc.code}.") from exc
        except urllib.error.URLError as exc:
            raise MCPError("Nao foi possivel conectar ao servidor MCP.") from exc

        if not raw.strip():
            return {}, new_session_id

        return self._decode_response(raw), new_session_id

    def list_tools(self, limit: int = 8) -> list[MCPTool]:
        initialize_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "sistema-escolar-didatico",
                    "version": "1.0.0",
                },
            },
        }
        initialized_response, session_id = self._post(initialize_payload)
        if initialized_response.get("error"):
            raise MCPError("Falha no handshake MCP (initialize).")

        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
        # Nem todo servidor responde a notificacoes; por isso ignoramos erro aqui.
        try:
            self._post(initialized_notification, session_id=session_id)
        except MCPError:
            pass

        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }
        try:
            tools_response, _ = self._post(tools_payload, session_id=session_id)
        except MCPError:
            # Fallback para servidores que aceitam tools/list sem sessao.
            tools_response, _ = self._post(tools_payload)
        if tools_response.get("error"):
            raise MCPError("Servidor MCP nao permitiu listar ferramentas.")

        tools_raw = tools_response.get("result", {}).get("tools", [])
        result: list[MCPTool] = []
        for item in tools_raw[: max(limit, 0)]:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "(sem nome)"))
            description = item.get("description")
            if description is not None:
                description = str(description)
            result.append(MCPTool(name=name, description=description))

        return result

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        initialize_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "sistema-escolar-didatico",
                    "version": "1.0.0",
                },
            },
        }
        initialized_response, session_id = self._post(initialize_payload)
        if initialized_response.get("error"):
            raise MCPError("Falha no handshake MCP (initialize).")

        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
        try:
            self._post(initialized_notification, session_id=session_id)
        except MCPError:
            pass

        call_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }
        call_response, _ = self._post(call_payload, session_id=session_id)
        if call_response.get("error"):
            message = call_response.get("error", {}).get("message", "Falha ao chamar tool MCP.")
            raise MCPError(str(message))

        result = call_response.get("result")
        if not isinstance(result, dict):
            raise MCPError("Resposta invalida ao chamar tool MCP.")

        return result

    def cadastrar_aluno(self, matricula: str, nome: str) -> dict[str, Any]:
        return self.call_tool(
            tool_name="cadastrar_aluno",
            arguments={"matricula": matricula, "nome": nome},
        )
