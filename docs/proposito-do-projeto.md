# Proposito do projeto

Este repositorio contem um sistema escolar didatico em Python, criado para estudar uma aplicacao simples com cadastro de alunos, lancamento de notas, calculo de media e consulta de situacao. O mesmo dominio e atendido por duas interfaces: uma linha de comando para uso no terminal e uma interface web em Flask.

## O que o sistema faz

- cadastra alunos por matricula e nome
- registra notas para um aluno existente
- calcula media automaticamente a partir das notas
- define a situacao do aluno como Aprovado ou Reprovado
- lista alunos cadastrados em ordem alfabetica
- mostra o detalhe de um aluno especifico
- persiste os dados em arquivo JSON
- possui testes automatizados para as regras centrais

## Como a aplicacao esta organizada

A logica principal fica separada em camadas para manter o projeto simples e facil de estudar:

- `sistema_escolar/models.py` define o modelo `Aluno`, com nome, matricula, notas, media e situacao
- `sistema_escolar/repository.py` faz leitura e escrita dos dados em `dados/alunos.json`
- `sistema_escolar/service.py` concentra as regras de negocio, como validar matricula, nome e notas
- `sistema_escolar/cli.py` oferece a interface de terminal
- `sistema_escolar/web.py` oferece a interface web com login simples, cadastro, lancamento de notas e dashboard
- `tests/test_service.py` valida o comportamento principal do servico

## Execucao

O projeto pode ser executado de duas formas:

- terminal: `python -m sistema_escolar.cli`
- web: `python -m sistema_escolar.web`

As dependencias devem ser instaladas com `python -m pip install -r requirements.txt`.

## Testes

Os testes automatizados sao executados com:

```powershell
python -m unittest discover -s tests -v
```

## Limites atuais

O projeto e propositalmente didatico e enxuto. Pelo codigo atual, ele trabalha com:

- armazenamento local em JSON
- credenciais fixas em memoria na interface web
- um conjunto pequeno de operacoes focadas em cadastro, notas e consulta

## Resumo

O objetivo do sistema e servir como exemplo de aplicacao escolar com separacao de responsabilidades, persistencia simples e validacao de regras basicas, reaproveitando a mesma logica de negocio na interface de terminal e na web.