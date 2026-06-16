# Exemplo didatico de sistema em Python

Este repositorio contem um sistema escolar simples, feito para estudo, com:

- cadastro de alunos
- lancamento de notas
- calculo de media e situacao
- persistencia em arquivo JSON
- testes automatizados
- exemplo de integracao com MCP publico

## Requisitos

- Python 3.11+

## Como executar

No terminal, na pasta do projeto:

```powershell
python -m sistema_escolar.cli
```

Para abrir a interface web:

```powershell
python -m sistema_escolar.web
```

Se for a primeira vez, instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

O sistema salva os dados em `dados/alunos.json`.

## Microservices (fase inicial de decomposicao)

Foi adicionada uma primeira extracao do monolito em dois servicos Flask independentes:

- `sistema_escolar/microservices/alunos_service.py`
- `sistema_escolar/microservices/notas_service.py`

Cada servico possui persistencia propria em JSON:

- Alunos Service: `dados/alunos_service.json`
- Notas Service: `dados/notas_service.json`

### Alunos Service

Executar:

```powershell
python -m sistema_escolar.microservices.alunos_service
```

Porta padrao: `8002`

Endpoints:

- `GET /health`
- `POST /alunos`
- `GET /alunos`
- `GET /alunos/<matricula>`

### Notas Service

Executar:

```powershell
python -m sistema_escolar.microservices.notas_service
```

Porta padrao: `8003`

Endpoints:

- `GET /health`
- `POST /notas`
- `GET /notas/<matricula>`

O Notas Service valida se o aluno existe consultando o Alunos Service.
Para mudar a URL do Alunos Service:

```powershell
$env:ALUNOS_SERVICE_URL = "http://127.0.0.1:8002"
python -m sistema_escolar.microservices.notas_service
```

## Servidor MCP local da aplicacao

Foi adicionado um servidor MCP HTTP local em `sistema_escolar/mcp_server.py` com a tool `cadastrar_aluno`.

Para iniciar o servidor:

```powershell
python -m sistema_escolar.mcp_server
```

Endpoint MCP:

```text
http://127.0.0.1:8001/mcp
```

Tool disponivel:

- `cadastrar_aluno`
	- argumentos: `matricula` (string), `nome` (string)
	- comportamento: reaproveita as regras de negocio existentes e salva em `dados/alunos.json`

### Cliente MCP local (linha de comando)

Tambem foi adicionado um cliente para chamar o servidor MCP local:

```powershell
python -m sistema_escolar.mcp_cli cadastrar-aluno 001 "Ana"
```

Se quiser usar outro endpoint:

```powershell
python -m sistema_escolar.mcp_cli --endpoint http://127.0.0.1:8001/mcp cadastrar-aluno 001 "Ana"
```

## Exemplo didatico de MCP

A interface web inclui a rota `/mcp-demo`, que faz um handshake MCP e lista ferramentas de um servidor publico.

Por padrao, o endpoint usado e:

```text
https://mcp.deepwiki.com/mcp
```

Observacao: o cliente da demo aceita respostas MCP em JSON e em SSE (`text/event-stream`).

Para trocar o servidor MCP, defina a variavel de ambiente `MCP_DEMO_URL` antes de iniciar a aplicacao web.

Exemplo no PowerShell:

```powershell
$env:MCP_DEMO_URL = "https://seu-servidor-mcp-publico/mcp"
python -m sistema_escolar.web
```

Depois de logar, abra o painel e clique em **Abrir demo MCP**.

## Como rodar os testes

```powershell
python -m unittest discover -s tests -v
```

## Estrutura

- `sistema_escolar/models.py`: modelo `Aluno`
- `sistema_escolar/repository.py`: leitura/escrita em JSON
- `sistema_escolar/service.py`: regras de negocio
- `sistema_escolar/cli.py`: interface no terminal
- `tests/test_service.py`: testes de unidade

## Sugestoes de estudo

1. Adicionar remocao de aluno.
2. Adicionar edicao de notas.
3. Criar exportacao para CSV.
4. Criar API com FastAPI reaproveitando `service.py`.
