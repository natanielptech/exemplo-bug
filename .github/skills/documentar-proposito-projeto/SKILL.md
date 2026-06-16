---
name: documentar-proposito-projeto
description: Gera documentacao em portugues explicando o proposito de um projeto com base no codigo-fonte, destacando objetivo, funcionalidades, arquitetura, execucao e limites.
---

# Documentar Proposito do Projeto

## Objetivo

Use esta skill quando for necessario documentar, em linguagem clara e objetiva, qual e o proposito de um projeto a partir da analise do codigo-fonte. A resposta deve refletir somente o que o codigo mostra, sem inventar funcionalidades nao implementadas.

## O que analisar

- `README.md`
- pontos de entrada da aplicacao
- modelos, servicos e repositorios centrais
- testes existentes
- arquivos de interface web e de terminal, quando existirem

## Como produzir a documentacao

1. Identifique o dominio do sistema e o problema que ele resolve.
2. Resuma as funcionalidades principais.
3. Explique a arquitetura em alto nivel e os modos de execucao.
4. Cite persistencia, dependencias e fluxo principal quando aparecerem no codigo.
5. Observe o que os testes confirmam sobre o comportamento.
6. Mencione limites ou ausencias importantes apenas se estiverem claros no codigo.

## Formato de saida sugerido

- Titulo curto do projeto
- Proposito em 1 paragrafo
- Lista das capacidades principais
- Resumo da arquitetura ou dos componentes
- Como executar e testar, se isso estiver evidente no codigo
- Observacoes sobre limites atuais do projeto

## Regras

- Escreva em portugues do Brasil.
- Priorize clareza e concisao.
- Baseie a saida apenas no codigo e na documentacao existente.
- Nao cite detalhes que nao possam ser confirmados.
- Se houver multiplas interfaces, explique como cada uma apoia o mesmo objetivo do sistema.
