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
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified:
#   - d4jules/core/crawler.py
# reference_documents_consulted:
#   - jules-flow/working-plan.md
# execution_details: |
#   Criada (ou atualizada) a classe `Crawler` em `d4jules/core/crawler.py`.
#   Adicionados atributos `self.to_visit_queue` (usando `collections.deque`) e `self.visited_urls` (usando `set`).
#   Implementados métodos:
#     - `add_url_to_visit(url)`: Adiciona à fila se não visitada e não na fila.
#     - `get_next_url()`: Retorna e remove da fila, ou None se vazia.
#     - `mark_as_visited(url)`: Adiciona ao set de visitadas.
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
