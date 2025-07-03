---
id: task-TNEW05_crawler_unit
title: "Reescrever testes unitários para src/core/crawler.py"
type: test
status: backlog
priority: high
dependencies: ["task-D10", "task-FIX01"] # Depends on the crawler implementation
parent_plan_objective_id: null
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "crawler", "unit-test", "core"]
description: |
  Reescrever os testes unitários para a classe `Crawler` em `src/core/crawler.py`.
  Estes testes focam em métodos individuais e lógica interna da classe, sem mocks extensivos de dependências externas (que seriam cobertos em testes de integração).
  Os testes originais (`tests/core/test_crawler_unit.py`) foram apagados.

  **Funcionalidades a serem testadas (com base no `tests/core/test_crawler_unit.py` original):**
  1.  **Inicialização (`__init__`):**
      - Verificar estado inicial da fila (`to_visit_queue`), `visited_urls`, `_queue_set`.
      - Verificar se `base_url` é adicionado à fila na inicialização.
      - Verificar `max_pages`, `max_depth` (se passados na inicialização, embora o teste original não focasse nisso, mas sim no `start_crawling` do teste de integração).
  2.  **Normalização de URL (`_normalize_url`):**
      - Variações de esquema (http, https), case do netloc.
      - Remoção de fragmentos (#).
      - Adição de trailing slash para domínios raiz.
      - Tratamento de URLs inválidas ou esquemas não suportados (deve retornar string vazia).
      - URLs com e sem www.
      - Caminhos com `.` e `..` (comportamento esperado do `urlparse`).
      - URLs com case diferente no path.
  3.  **Adição de URLs (`add_url`, `add_urls`):**
      - Adicionar URL válida e nova (verificar fila e `_queue_set`).
      - Não adicionar URL já visitada.
      - Não adicionar URL já presente na fila (`_queue_set`).
      - Não adicionar URLs inválidas ou vazias.
      - Adicionar uma lista de URLs, tratando duplicatas dentro da lista e em relação ao estado atual.
  4.  **Recuperação de URL (`get_next_url`):**
      - Verificar ordem FIFO.
      - Verificar se URL é removida da fila e de `_queue_set`.
      - Verificar se URL é adicionada a `visited_urls`.
      - Retornar `None` se a fila estiver vazia.
  5.  **Marcação de Visitadas (`mark_as_visited`):**
      - Verificar se a URL (normalizada) é adicionada a `visited_urls`.
  6.  **Status da Fila (`has_next_url`, `get_queue_size`, `get_visited_count`):**
      - Testar em diferentes cenários (fila vazia, com itens, após `get_next_url`).
  7.  **Verificação de Domínio (`can_crawl_url`):**
      - URLs no mesmo domínio do `base_url`.
      - URLs em subdomínios diferentes (deve retornar `False` se `base_url` não for o subdomínio).
      - URLs em domínios diferentes.
      - Comportamento quando `base_url` não está definido no Crawler (deve permitir qualquer URL).

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/core/test_crawler_unit.py`.
  - Utilizar `unittest`.
  - Foco em testes de estado e lógica interna, com mínima necessidade de mocks.

## Critérios de Aceitação
- Cobertura completa dos métodos públicos e da lógica de normalização/gerenciamento de URLs.
- Os testes validam o comportamento da classe `Crawler` em isolamento.
- Os testes passam consistentemente.
---
