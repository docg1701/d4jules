---
id: task-T12
title: "Testes para a task-D10: Gerenciamento de Fila de URLs e Controle de Visitas"
type: test
status: in_progress # Field from original file, actual status managed by task-index.md
priority: medium
dependencies: ["task-D10", "task-FIX01"]
parent_plan_objective_id: "3.4.1" # Referencing parent objective of D10
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "crawler", "core"]
description: |
  Testar a classe `Crawler` em `src/core/crawler.py`.
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
  5. Verificação de escopo de domínio (`can_crawl_url`).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "All tests implemented and passed after minor adjustments to crawler.py and test expectations."
# start_time: 2024-07-29T12:00:00Z # Placeholder
# end_time: 2024-07-29T13:00:00Z # Placeholder
# duration_minutes: 60 # Placeholder
# files_modified:
#   - src/core/crawler.py
#   - tests/core/test_crawler.py
# reference_documents_consulted:
#   - jules-flow/done/task-D10.md
#   - src/core/crawler.py
#   - jules-flow/in_progress/task-T12.md (for test criteria)
# execution_details: |
#   1. Created `tests/core/test_crawler.py` with initial structure.
#   2. Implemented 10 test methods for `Crawler` class:
#      - `test_initialization_empty`
#      - `test_initialization_with_base_url`
#      - `test_normalize_url` (testing `_normalize_url` via direct calls for clarity)
#      - `test_add_url_and_get_next_url`
#      - `test_add_url_duplicates_and_visited`
#      - `test_add_invalid_urls`
#      - `test_add_urls_list`
#      - `test_mark_as_visited`
#      - `test_state_methods`
#      - `test_can_crawl_url_domain_scoping`
#   3. Adjusted one normalization test case (`http://example.com/a/./b/../c`) to reflect that `_normalize_url` does not currently simplify `.` or `..` path segments.
#   4. Ran tests. Two failures occurred:
#      - `test_add_urls_list`: Expected 2 URLs in queue, got 3. Realized that path casing is preserved by `_normalize_url` (e.g., `/p2` vs `/P2`), so 3 was correct. Updated test assertion.
#      - `test_can_crawl_url_domain_scoping`: `crawler_no_base.can_crawl_url("ftp://invalid.scheme.com")` returned `True` instead of expected `False`.
#   5. Modified `src/core/crawler.py` in `can_crawl_url` method: added a check at the beginning to return `False` if `_normalize_url(url)` results in an empty string (i.e., the URL is invalid by normalization standards), before checking if `base_url` is set. This makes `can_crawl_url` more robust for invalid schemes even without a base_url for scoping.
#   6. Re-ran tests. All 10 tests passed.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/crawler.py` (leitura/modificação)
* `tests/core/test_crawler.py` (criação/modificação)

## Critérios de Aceitação
1.  `tests/core/test_crawler.py` é criado.
2.  A normalização de URL (`_normalize_url`) é testada com diferentes cenários (http, https, sem scheme, com/sem fragmento, com/sem trailing slash, case insensitivity para scheme/netloc).
3.  `add_url` adiciona corretamente URLs novas e normalizadas à fila e ao `_queue_set`.
4.  `add_url` ignora URLs nulas, vazias, ou que resultam em string vazia após normalização.
5.  `add_url` não adiciona URLs que já estão no `visited_urls`.
6.  `add_url` não adiciona URLs que já estão no `_queue_set`.
7.  `get_next_url` retorna URLs na ordem correta (FIFO) e as remove da fila e do `_queue_set`, adicionando-as ao `visited_urls`.
8.  `get_next_url` retorna `None` quando a fila está vazia.
9.  `mark_as_visited` adiciona a URL normalizada ao `visited_urls`.
10. Métodos auxiliares (`has_next_url`, `get_queue_size`, `get_visited_count`) retornam os valores corretos.
11. O método `can_crawl_url` é testado para URLs dentro e fora do domínio base, e quando não há domínio base.
12. Todos os testes passam.

## Observações Adicionais
Esta classe é fundamental para o controle do processo de crawling.
O item 5 na seção de descrição ("Correta normalização de URLs...") foi expandido nos critérios de aceitação.
O critério de aceitação 11 (originalmente sobre `can_crawl_url` sendo testado) foi adicionado explicitamente.
O antigo critério 11 ("Todos os testes passam") tornou-se o critério 12.
```
