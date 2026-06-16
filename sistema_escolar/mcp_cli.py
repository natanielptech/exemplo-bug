from __future__ import annotations

import argparse

from sistema_escolar.mcp_client import MCPDemoClient, MCPError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cliente MCP local do sistema escolar")
    parser.add_argument(
        "--endpoint",
        default="http://127.0.0.1:8001/mcp",
        help="Endpoint MCP HTTP",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    cadastrar = subparsers.add_parser(
        "cadastrar-aluno",
        help="Cadastra aluno via tool MCP cadastrar_aluno",
    )
    cadastrar.add_argument("matricula", help="Matricula do aluno")
    cadastrar.add_argument("nome", help="Nome do aluno")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    client = MCPDemoClient(endpoint=args.endpoint)

    try:
        if args.command == "cadastrar-aluno":
            result = client.cadastrar_aluno(args.matricula, args.nome)
            if result.get("isError"):
                content = result.get("content") or []
                mensagem = "Falha ao cadastrar aluno."
                if content and isinstance(content[0], dict):
                    mensagem = str(content[0].get("text", mensagem))
                print(mensagem)
                return 1

            structured = result.get("structuredContent") or {}
            nome = structured.get("nome", args.nome)
            matricula = structured.get("matricula", args.matricula)
            print(f"Aluno cadastrado: {nome} ({matricula})")
            return 0

        parser.print_help()
        return 2
    except MCPError as exc:
        print(f"Erro MCP: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())