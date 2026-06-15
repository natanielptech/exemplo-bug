# Exemplo didatico de sistema em Python

Este repositorio contem um sistema escolar simples, feito para estudo, com:

- cadastro de alunos
- lancamento de notas
- calculo de media e situacao
- persistencia em arquivo JSON
- testes automatizados

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
