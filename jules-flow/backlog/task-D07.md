---
id: task-D07
title: "Implementar carregamento de config.ini em scraper_cli.py"
type: development
status: backlog
priority: high
dependencies: ["task-D01", "task-D02"] # D01 cria d4jules/, D02 cria config.ini
parent_plan_objective_id: "3.1"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "config", "core"]
description: |
  Implementar a lógica inicial no script `d4jules/scraper_cli.py` para carregar as configurações do arquivo `d4jules/config.ini`.
  Utilizar a biblioteca `configparser` do Python.
  A função de carregamento deve ler:
  - `api_key` da seção `[GOOGLE_AI]`.
  - `model_name` da seção `[LLM]`.
  Esses valores devem ser armazenados de forma acessível para o restante da aplicação.

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
#   - d4jules/core/config_loader.py (ou similar, se modularizado)
# reference_documents_consulted:
#   - jules-flow/working-plan.md
#   - task-D02.md (para estrutura do config.ini)
# execution_details: |
#   Criado `d4jules/scraper_cli.py` (inicialmente).
#   Implementada função (possivelmente em `d4jules/core/config_loader.py` e importada)
#   para usar `configparser` para ler `d4jules/config.ini`.
#   A função retorna um dicionário ou objeto com as configurações.
#   Adicionado tratamento básico de erro para arquivo não encontrado ou seção/chave ausente.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/scraper_cli.py` (criação/modificação)
* `d4jules/config.ini` (leitura)
* Opcional: `d4jules/core/config_loader.py` (se a lógica for modularizada)

## Critérios de Aceitação
1.  Criação do arquivo `d4jules/scraper_cli.py` (se ainda não existir).
2.  Uma função é implementada para ler o arquivo `d4jules/config.ini`.
3.  A função extrai corretamente `api_key` de `[GOOGLE_AI]` e `model_name` de `[LLM]`.
4.  A função lida de forma graciosa com o arquivo `config.ini` não encontrado ou com seções/chaves ausentes (ex: logando um erro e saindo, ou retornando valores padrão/None).
5.  Testes unitários (se aplicável e o ambiente permitir) para a função de carregamento de configuração.

## Observações Adicionais
Esta é uma das primeiras funcionalidades do `scraper_cli.py`.
```
