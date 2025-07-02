---
id: task-D10
title: "Implementar gerenciamento de fila de URLs e controle de visitas"
type: development
status: backlog
priority: medium
dependencies: []
parent_plan_objective_id: "3.4.1"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "crawler", "core"]
description: |
  Desenvolver a lógica para gerenciar a fila de URLs a serem visitadas pelo crawler e para controlar as URLs que já foram visitadas.
  Esta funcionalidade pode ser parte de uma classe `Crawler` em `d4jules/core/crawler.py` ou um conjunto de funções.
  Deve incluir:
  1. Uma estrutura de dados para a fila de URLs (ex: `collections.deque`).
  2. Uma estrutura de dados para armazenar URLs visitadas (ex: `set`) para evitar reprocessamento e loops.
  3. Métodos/funções para adicionar URLs à fila (verificando se já não foi visitada ou já está na fila).
  4. Método/função para obter a próxima URL da fila.
  5. Método/função para marcar uma URL como visitada.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-02T19:00:00Z # Estimado
# end_time: 2024-07-02T19:30:00Z # Estimado
# duration_minutes: 30 # Estimado
# files_modified:
#   - d4jules/src/core/crawler.py
#   - d4jules/src/core/__init__.py
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D10.md
#   - VISION.md
# execution_details: |
#   1. Criado o arquivo `d4jules/src/core/crawler.py`.
#   2. Implementada a classe `Crawler` com:
#      - `__init__(self)`: Inicializa `self.to_visit_queue` (collections.deque), `self.visited_urls` (set), e `self._queue_set` (set para verificação rápida de presença na fila).
#      - `_normalize_url(self, url: str) -> str`: Normaliza URLs (scheme, netloc lowercase, remove fragmentos e trailing slashes). Retorna string vazia para schemes não http/https.
#      - `add_url(self, url: str)`: Adiciona URL normalizada à fila e `_queue_set` se não visitada e não já na fila.
#      - `add_urls(self, urls: list[str])`: Helper para adicionar múltiplas URLs.
#      - `get_next_url(self) -> str | None`: Remove e retorna a próxima URL da fila, marca como visitada, e remove de `_queue_set`.
#      - `mark_as_visited(self, url: str)`: Adiciona URL normalizada ao `visited_urls`.
#      - `has_next_url(self) -> bool`: Verifica se a fila não está vazia.
#      - `get_queue_size(self) -> int`: Retorna o tamanho da fila.
#      - `get_visited_count(self) -> int`: Retorna o número de URLs visitadas.
#   3. Adicionado um bloco `if __name__ == "__main__":` em `crawler.py` para demonstração básica.
#   4. Atualizado `d4jules/src/core/__init__.py` para exportar a classe `Crawler`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/core/crawler.py` (criação/modificação)

## Critérios de Aceitação
1.  Implementação de uma fila para URLs a visitar.
2.  Implementação de um conjunto para URLs visitadas.
3.  Lógica para adicionar URLs à fila apenas se não tiverem sido visitadas e não estiverem já na fila.
4.  Lógica para recuperar a próxima URL da fila e marcá-la como visitada.
5.  A estrutura deve ser eficiente para as operações de adição e verificação.

## Observações Adicionais
Esta é uma componente central do crawler.
```
