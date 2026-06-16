---
name: separar-monolito-em-microservices
description: "Use when planning or executing the decomposition of this school monolith into microservices, with practical boundaries, migration strategy, contracts, testing, and operations best practices for the current Python/Flask stack."
---

# Separar Monolito em Microservices

## Objetivo

Use esta skill para planejar e implementar a separacao do projeto `exemplo-bug` em microservices, com foco no dominio atual:

- cadastro de alunos
- lancamento e consulta de notas

A skill deve priorizar seguranca de migracao, baixo acoplamento e evolucao incremental sem quebrar funcionalidades existentes.

## Contexto da stack atual

- Linguagem: Python 3.11+
- Web: Flask
- Persistencia atual: JSON local
- Testes: `unittest`
- Modulos centrais atuais:
  - `sistema_escolar/service.py`
  - `sistema_escolar/repository.py`
  - `sistema_escolar/web.py`

## Quando usar

Use esta skill quando o pedido envolver:

- separar cadastro e notas em servicos independentes
- definir limites de dominio e ownership de dados
- criar estrategia de migracao do monolito para microservices
- desenhar contratos HTTP/eventos entre servicos
- reduzir acoplamento entre modulos atuais

## Principios obrigatorios

1. Decompor por capacidade de negocio, nao por camada tecnica.
2. Cada microservice deve ter ownership exclusivo de seus dados.
3. Nao compartilhar banco/arquivo entre servicos.
4. Contratos de API devem ser explicitos e versionados.
5. Mudancas devem ser incrementais com compatibilidade retroativa.
6. Observabilidade e testes de contrato sao obrigatorios desde o inicio.

## Recorte recomendado para este projeto

### 1) Alunos Service

Responsavel por:

- cadastrar aluno
- consultar aluno
- listar alunos

Dados proprios:

- identificacao e dados cadastrais do aluno

### 2) Notas Service

Responsavel por:

- lancar nota
- consultar notas por aluno
- calcular media e status

Dados proprios:

- historico de notas e metadados de avaliacao

Dependencia externa:

- validacao de existencia de aluno via API do Alunos Service

## Estrategia de migracao (Strangler Fig)

1. Mapeie casos de uso no monolito e classifique por dominio.
2. Extraia primeiro o Alunos Service mantendo o monolito funcional.
3. Adicione um adaptador no monolito para consumir o novo servico.
4. Extraia o Notas Service e substitua chamadas internas por HTTP entre servicos.
5. Congele novos acoplamentos no monolito legado.
6. Remova codigo legado apenas apos cobertura de testes e monitoracao estavel.

## Contratos e comunicacao

- Sincrono: REST/JSON com timeout, retry com backoff e tratamento de erro claro.
- Assincrono (quando necessario): eventos de dominio simples, ex. `aluno_cadastrado`.
- Idempotencia para operacoes de escrita sensiveis.
- Correlation ID para rastreio entre servicos.

## Boas praticas de implementacao

- Estrutura por servico:
  - `app` (rotas/controladores)
  - `domain` (regras de negocio)
  - `infra` (repositorio, cliente HTTP, persistencia)
  - `tests` (unitario, integracao, contrato)
- Configuracao por variaveis de ambiente.
- Health endpoints (`/health`, `/ready`).
- Logs estruturados e metricas basicas (latencia, erro, throughput).
- Evitar transacoes distribuidas; preferir consistencia eventual e compensacao.

## Testes minimos por etapa

1. Unitarios para regras de negocio de cada servico.
2. Integracao para repositorio e rotas HTTP.
3. Contrato consumidor-provedor entre Alunos Service e Notas Service.
4. Regressao no monolito durante periodo de transicao.

Comando base mantido no projeto:

- `python -m unittest discover -s tests -v`

## Checklist de prontidao para cada microservice

- Limites de dominio claros e sem ambiguidades
- API documentada e versionada
- Dados isolados
- Telemetria minima ativa
- CI com testes unitarios + integracao + contrato
- Plano de rollback definido

## Formato de resposta esperado ao usar esta skill

Ao receber uma solicitacao de separacao para microservices, entregue:

1. mapa de modulos atuais para novos servicos
2. plano incremental em fases com risco e mitigacao
3. definicao inicial de contratos (endpoints/payloads/eventos)
4. mudancas de codigo propostas por fase
5. estrategia de testes e criterios de aceite

## Regras de qualidade

- Escreva explicacoes em portugues do Brasil.
- Evite reescrita total: preferir extracao incremental.
- Nao compartilhar modelos de dominio entre servicos por import direto.
- Nao introduzir dependencia operacional desnecessaria para um projeto didatico.