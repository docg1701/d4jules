---
id: task-T11
title: "Testes para a task-D08: Solicitação de URL ao usuário em scraper_cli.py"
type: test
status: backlog
priority: medium
dependencies: ["task-D08"]
parent_plan_objective_id: "3.2" # Referencing parent objective of D08
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "cli", "interaction", "validation"]
description: |
  Testar a funcionalidade de solicitação e validação básica de URL no script `d4jules/scraper_cli.py`.
  Os testes devem verificar:
  1. Carregamento de configuração (mockando `load_config` para retornar sucesso ou erro).
  2. Exibição do prompt para inserção de URL.
  3. Comportamento da função `get_user_url()` com diferentes entradas (válidas e inválidas), mockando a função `input()`.
  4. Exibição da URL validada.

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
#   - tests/test_scraper_cli_url_input.py (ou similar)
# reference_documents_consulted:
#   - jules-flow/done/task-D08.md
#   - d4jules/scraper_cli.py
# execution_details: |
#   1. Criado arquivo de teste (ex: `tests/test_scraper_cli_url_input.py`).
#   2. Testes para `main()`:
#      - Mock `load_config` para simular sucesso e falha no carregamento de config.
#      - Mock `get_user_url` para controlar a URL retornada.
#      - Verificar se as mensagens corretas são impressas.
#   3. Testes para `get_user_url()`:
#      - Mock `input()` com `unittest.mock.patch('builtins.input')`.
#      - Testar com URL válida (http, https).
#      - Testar com URL vazia (espera reprompt).
#      - Testar com URL sem prefixo http/https (espera reprompt ou sugestão).
#      - Testar com URL com http mas sem domínio (espera reprompt).
#      - Testar cancelamento com Ctrl+C (mock `input` para levantar `KeyboardInterrupt`, verificar `sys.exit`).
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/scraper_cli.py` (leitura)
* `d4jules/src/core/config_loader.py` (para mockar `load_config`)
* `tests/test_scraper_cli_url_input.py` (criação/modificação)

## Critérios de Aceitação
1.  Testes unitários verificam que `scraper_cli.py` chama `load_config` e lida com `ConfigError`.
2.  Testes unitários (mockando `input`) verificam que `get_user_url()`:
    a.  Retorna uma URL válida quando fornecida.
    b.  Re-solicita a URL se a entrada estiver vazia.
    c.  Re-solicita a URL ou sugere correção se o prefixo "http://" ou "https://" estiver ausente.
    d.  Re-solicita se a URL parecer incompleta (ex: sem domínio).
3.  Testes unitários verificam que `main()` imprime a URL validada ou sai se nenhuma URL for fornecida.
4.  Todos os testes relevantes passam.

## Observações Adicionais
Será necessário usar `unittest.mock.patch` extensivamente para `load_config` e `builtins.input`.
```
