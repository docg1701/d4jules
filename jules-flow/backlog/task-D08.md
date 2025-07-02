---
id: task-D08
title: "Implementar solicitação de URL ao usuário em scraper_cli.py"
type: development
status: backlog
priority: medium
dependencies: ["task-D07"] # Assume que scraper_cli.py já foi iniciado
parent_plan_objective_id: "3.2"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "cli", "interaction"]
description: |
  No script `d4jules/scraper_cli.py`, adicionar a funcionalidade para interagir com o usuário e solicitar a URL do site de documentação que deve ser processado.
  Utilizar a função `input()` do Python para capturar a URL fornecida pelo usuário.
  A URL deve ser armazenada em uma variável para uso posterior.

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
#   - d4jules/scraper_cli.py
# reference_documents_consulted:
#   - jules-flow/working-plan.md
# execution_details: |
#   Adicionada lógica ao `main()` ou função apropriada em `d4jules/scraper_cli.py`
#   para exibir uma mensagem ao usuário e capturar a entrada da URL via `input()`.
#   A URL é armazenada em uma variável.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/scraper_cli.py` (modificação)

## Critérios de Aceitação
1.  O script `d4jules/scraper_cli.py`, quando executado, solicita ao usuário que insira uma URL.
2.  A URL fornecida pelo usuário é lida e armazenada corretamente em uma variável.
3.  A solicitação é clara e informativa para o usuário.

## Observações Adicionais
Validação básica da URL (ex: se não está vazia) pode ser considerada, mas validação extensiva (formato, acessibilidade) pode ser uma task separada ou parte da lógica de download.
```
