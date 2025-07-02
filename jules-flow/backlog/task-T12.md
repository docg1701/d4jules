---
id: task-T12
title: "Testes para a task-D10: Gerenciamento de Fila de URLs e Controle de Visitas"
type: test
status: backlog
priority: medium
dependencies: ["task-D10"]
parent_plan_objective_id: "3.4.1" # Referencing parent objective of D10
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "crawler", "core"]
description: |
  Testar a classe `Crawler` em `d4jules/src/core/crawler.py`.
  Os testes devem cobrir:
  1. Adição de URLs à fila (`add_url`, `add_urls`):
     - Adição de URL válida e nova.
     - Tentativa de adicionar URL já visitada (não deve ser adicionada).
     - Tentativa de adicionar URL já presente na fila (não deve ser adicionada).
     - Tratamento de URLs inválidas ou vazias (não devem ser adicionadas).
     - Correta normalização de URLs (remoção de fragmentos, remoção de trailing slashes, lowercase de scheme/netloc, adição de scheme https padrão).
  2. Obtenção da próxima URL (`get_next_url`):
     - Retorno de URLs em ordem FIFO.
     - Retorno de `None` se a fila estiver vazia.
     - URL recuperada é marcada como visitada e removida da "presença na fila" (`_queue_set`).
  3. Marcação de URLs como visitadas (`mark_as_visited`):
     - URL é adicionada ao conjunto de visitadas e normalizada.
  4. Verificação de estado (`has_next_url`, `get_queue_size`, `get_visited_count`).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified:
#   - tests/test_crawler.py
# reference_documents_consulted:
#   - jules-flow/done/task-D10.md
#   - d4jules/src/core/crawler.py
# execution_details: |
#   1. Criado `tests/test_crawler.py`.
#   2. Implementada a classe `TestCrawler(unittest.TestCase)`.
#   3. Testes para `_normalize_url` com vários casos.
#   4. Testes para `add_url` e `add_urls` cobrindo URLs válidas, inválidas, duplicadas na fila, já visitadas.
#   5. Testes para `get_next_url` verificando ordem FIFO, remoção da fila, adição a visitadas, e retorno de None para fila vazia.
#   6. Testes para `mark_as_visited`.
#   7. Testes para `has_next_url`, `get_queue_size`, `get_visited_count`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/src/core/crawler.py` (leitura)
* `tests/test_crawler.py` (criação/modificação)

## Critérios de Aceitação
1.  `test_crawler.py` é criado em `tests/`.
2.  A normalização de URL (`_normalize_url`) é testada com diferentes cenários (http, https, sem scheme, com/sem fragmento, com/sem trailing slash, case insensitivity para scheme/netloc).
3.  `add_url` adiciona corretamente URLs novas e normalizadas à fila e ao `_queue_set`.
4.  `add_url` ignora URLs nulas, vazias, ou que resultam em string vazia após normalização.
5.  `add_url` não adiciona URLs que já estão no `visited_urls`.
6.  `add_url` não adiciona URLs que já estão no `_queue_set`.
7.  `get_next_url` retorna URLs na ordem correta (FIFO) e as remove da fila e do `_queue_set`, adicionando-as ao `visited_urls`.
8.  `get_next_url` retorna `None` quando a fila está vazia.
9.  `mark_as_visited` adiciona a URL normalizada ao `visited_urls`.
10. Métodos auxiliares (`has_next_url`, `get_queue_size`, `get_visited_count`) retornam os valores corretos.
11. Todos os testes passam.

## Observações Adicionais
Esta classe é fundamental para o controle do processo de crawling.
```
