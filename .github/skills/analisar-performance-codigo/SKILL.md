---
name: analisar-performance-codigo
description: Analisa codigo-fonte em busca de trechos nao performaticos, gargalos, operacoes desnecessarias e padroes ineficientes, sugerindo alteracoes objetivas de melhoria.
---

# Analisar Performance do Codigo

## Objetivo

Use esta skill quando for necessario inspecionar codigo e apontar trechos que possam estar lentos, custando memoria, fazendo trabalho repetido ou usando estruturas inadequadas para o volume de dados esperado.

O foco e identificar oportunidades reais de melhoria e sugerir alteracoes claras, com base no que o codigo mostra.

## Quando usar

Use esta skill quando o pedido envolver:

- localizar codigo com possivel impacto negativo de performance
- revisar loops, consultas, acessos a disco, chamadas de rede ou processamento repetido
- comparar alternativas de implementacao com menor custo
- sugerir refatoracoes para reduzir complexidade temporal ou uso de memoria
- revisar codigo apos relato de lentidao, timeout ou consumo excessivo de recursos

## O que analisar

- loops aninhados e repeticao desnecessaria de processamento
- chamadas repetidas para mesma informacao dentro de laços ou mapas
- acesso frequente a disco, rede ou banco de dados dentro de fluxo quente
- consultas N+1 ou carregamento repetido de dados
- uso inadequado de listas quando `set`, `dict` ou `deque` seriam melhores
- concatenacao excessiva de strings em laços
- ordenacoes, filtros e transformacoes repetidas sem necessidade
- validacoes ou conversoes feitas varias vezes para o mesmo valor

## Como responder

1. Aponte o trecho problemático com linguagem objetiva.
2. Explique por que ele pode ser ineficiente.
3. Sugira a alteracao mais simples e segura.
4. Quando fizer sentido, ofereca uma alternativa mais escalavel.
5. Mencione o trade-off se a melhora aumentar complexidade ou reduzir legibilidade.

## Formato de saida sugerido

- achado principal
- impacto esperado
- sugestao de alteracao
- opcionalmente, exemplo de antes e depois
- observacao sobre risco ou trade-off

## Regras

- Escreva em portugues do Brasil.
- Baseie a analise apenas no codigo e no contexto visivel.
- Nao suponha medicao real se nao houver evidencia.
- Diferencie suspeita de problema confirmado.
- Priorize mudancas pequenas que tragam ganho claro.
- Se nao houver gargalo evidente, diga que nao encontrou problema performatico claro e indique onde valeria medir.

## Checklist

- O trecho lento foi identificado com clareza
- A causa da ineficiencia foi explicada
- A sugestao reduz custo de tempo, memoria ou IO
- O impacto da mudanca foi descrito de forma honesta
- Nao foram feitas promessas sem base no codigo
