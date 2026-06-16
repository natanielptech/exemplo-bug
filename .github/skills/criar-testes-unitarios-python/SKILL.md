---
name: criar-testes-unitarios-python
description: "Use when creating, reviewing, or improving Python unit tests in this project, especially for business rules, isolated data, unittest, Flask test client, and quality test practices."
---

# Criar Testes Unitarios para Este Projeto

## Objetivo

Use esta skill para criar, revisar e melhorar testes unitarios no projeto `exemplo-bug`, respeitando a stack atual e as convencoes ja usadas no repositorio.

Esta skill deve priorizar:

- confiabilidade dos testes
- isolamento entre casos
- legibilidade e manutencao
- cobertura de regras de negocio criticas

## Stack e Convencoes do Projeto

- Linguagem: Python 3.11+
- Framework web: Flask (interface web em `sistema_escolar/web.py`)
- Runner atual: `unittest` com descoberta em `tests/`
- Persistencia: JSON via `sistema_escolar/repository.py`
- Comando de testes atual:
  - `python -m unittest discover -s tests -v`

## Quando usar

Use esta skill quando o pedido envolver:

- criar novos testes unitarios para services, models, repository ou web
- ajustar testes apos mudancas de regra de negocio
- cobrir casos de erro (validacoes, excecoes, entradas invalidas)
- aumentar cobertura sem tornar testes frageis

## Principios obrigatorios

1. Testes devem ser deterministicos.
2. Cada teste valida um comportamento principal.
3. Evite dependencia entre testes.
4. Isole IO em recursos temporarios (ex.: `tempfile.TemporaryDirectory`).
5. Prefira asserts especificos e mensagens claras por intencao do nome do teste.
6. Cubra caminho feliz e caminho de falha para regras centrais.
7. Nao teste detalhe interno privado quando puder testar comportamento publico.

## Estrategia por camada

### Service (`sistema_escolar/service.py`)

Priorizar testes de regra de negocio:

- cadastro valido
- matricula duplicada
- nome invalido
- lancamento de nota fora de faixa
- media e situacao apos multiplas notas
- busca de aluno inexistente

### Repository (`sistema_escolar/repository.py`)

Focar em comportamento observavel:

- arquivo ausente inicializa colecao vazia
- persistencia apos salvar
- leitura consistente apos nova instancia
- resiliencia para arquivo vazio/corrompido (conforme comportamento esperado do projeto)

### Web (`sistema_escolar/web.py`)

Usar Flask test client para validar:

- status code correto
- renderizacao de conteudo essencial
- redirects esperados
- fluxo minimo de login e acesso protegido (se existir)
- mensagens de erro em entradas invalidas

## Padrao de escrita dos testes

1. Nome da classe: `<Componente>Tests`
2. Nome do teste: `test_<comportamento_esperado>`
3. Estrutura AAA:
   - Arrange: prepara dados e dependencias
   - Act: executa uma acao
   - Assert: valida resultado
4. Evitar logica complexa dentro do proprio teste.

## Template base para testes de service

```python
import tempfile
import unittest
from pathlib import Path

from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


class SistemaEscolarServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "alunos.json"
        self.sistema = SistemaEscolar(AlunoRepository(str(db_path)))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_exemplo(self) -> None:
        # Arrange
        self.sistema.cadastrar_aluno("001", "Ana")

        # Act
        aluno = self.sistema.buscar_aluno("001")

        # Assert
        self.assertEqual(aluno.nome, "Ana")
```

## Template base para testes web

```python
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
```

## Checklist antes de finalizar

- Arquivo de teste esta em `tests/test_<alvo>.py`
- Todos os testes passam localmente
- Nomes de testes descrevem comportamento
- Casos de sucesso e erro estao cobertos
- Nao ha dependencias externas nao controladas
- Setup/teardown limpam estado temporario

## Saida esperada ao usar esta skill

Ao responder uma solicitacao de testes, entregue:

1. lista dos comportamentos cobertos
2. codigo dos testes pronto para execucao
3. comando para rodar os testes relevantes
4. breve observacao de riscos nao cobertos (se houver)

## Regras de qualidade

- Escreva em portugues do Brasil quando explicar.
- Mantenha o codigo dos testes idiomatico para Python 3.11.
- Preserve o uso de `unittest` neste repositorio, salvo pedido explicito para migracao.
- Evite alterar codigo de producao sem necessidade para apenas "fazer teste passar".
