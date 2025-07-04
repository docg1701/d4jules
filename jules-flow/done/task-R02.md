---
id: task-R02
title: "Implementar Controle de Profundidade (max_depth) no Crawler"
type: refactor
status: backlog # Original status
priority: medium
dependencies: ["task-R01"]
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["crawler", "feature"]
description: |
  Adicionar a lógica para respeitar o parâmetro `max_depth` no `Crawler`.
  Atualmente, `max_depth` é carregado da configuração e passado para o construtor do `Crawler`, mas não é utilizado para limitar a profundidade do rastreamento.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-04T10:30:00Z # Estimativa
# end_time: 2024-07-04T11:00:00Z # Estimativa
# duration_minutes: 30 # Estimativa
# files_modified:
#   - src/core/crawler.py
#   - tests/core/test_crawler.py
# reference_documents_consulted: []
# execution_details: |
#   1. Modificado `src/core/crawler.py`:
#      - `__init__`: A URL base agora é adicionada à fila com `depth=0` usando `self.add_url(base_url, depth=0)`.
#      - `add_url(self, url: str, depth: int)`:
#        - Parâmetro `depth` adicionado.
#        - Antes de adicionar à fila, verifica se `self.max_depth` é `None` ou se `depth <= self.max_depth`.
#        - A fila `self.to_visit_queue` agora armazena tuplas `(normalized_url, depth)`.
#      - `add_urls(self, urls: list[str], current_depth: int)`:
#        - Parâmetro `current_depth` adicionado.
#        - Calcula `new_link_depth = current_depth + 1`.
#        - Adiciona uma verificação explícita para não adicionar links se `new_link_depth > self.max_depth`.
#        - Chama `self.add_url(url, new_link_depth)` para cada link.
#      - `get_next_url(self) -> Tuple[Optional[str], Optional[int]]`:
#        - Retorna uma tupla `(url, depth)` ou `(None, None)`.
#      - `start_crawling(self)`:
#        - Unpacks `current_url, current_depth` de `self.get_next_url()`.
#        - Passa `current_depth` para `self.add_urls()` ao adicionar novos links.
#        - Adicionada uma verificação de segurança no início do loop para pular URLs cuja profundidade já exceda `max_depth` (embora `add_url` deva prevenir isso).
#        - Mensagens de log/print atualizadas para incluir a profundidade.
#
#   2. Modificado `tests/core/test_crawler.py`:
#      - `test_add_url_and_get_next_url`: Atualizado para usar `add_url` com `depth` e esperar tuplas de `get_next_url`.
#      - `test_add_url_duplicates_and_visited`: Atualizado para usar `add_url` com `depth`.
#      - `test_add_invalid_urls`: Atualizado para usar `add_url` com `depth`.
#      - `test_add_urls_list`: Atualizado para chamar `add_urls` com `current_depth` e verificar se os links são adicionados com a profundidade correta.
#      - `test_state_methods`: Atualizado para usar `add_url` com `depth`.
#      - `test_start_crawling_successful_run_one_page`: Verificado se os novos links são adicionados com a profundidade correta.
#      - Adicionado `test_max_depth_limit`:
#        - Testa com `max_depth=0`: garante que apenas a URL base é processada e nenhum link novo (profundidade 1) é adicionado à fila para processamento.
#        - Testa com `max_depth=1`: garante que a URL base (profundidade 0) e seus links diretos (profundidade 1) são processados, mas links de profundidade 2 não são adicionados para processamento.
#
# A funcionalidade de `max_depth` está agora implementada e testada.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/crawler.py`

## Critérios de Aceitação
1. O `Crawler` deve armazenar a profundidade de cada URL em sua fila (ex: usando tuplas `(url, depth)`).
2. A URL inicial é adicionada com profundidade 0.
3. Ao processar uma URL de profundidade `d`, quaisquer novos links extraídos dessa página são adicionados à fila com profundidade `d + 1`.
4. Novas URLs só são adicionadas à fila se sua profundidade calculada (`d + 1`) for menor ou igual a `self.max_depth`. Se `self.max_depth` for `None`, não há limite de profundidade.
5. Testes unitários para o `Crawler` são atualizados ou criados para verificar o comportamento correto do `max_depth` (ex: não adicionar URLs além da profundidade, parar o crawling se todas as URLs restantes excederem a profundidade).

## Observações Adicionais
Considerar o caso em que `max_depth` é 0 (significando apenas a URL inicial deve ser processada).
O `max_depth` é um inteiro não negativo.
