---
id: task-D01
title: "Criar estrutura de diretórios base para d4jules"
type: development
status: backlog
priority: high
dependencies: []
parent_plan_objective_id: "1.1"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "setup", "structure"]
description: |
  Criar os diretórios principais para o projeto `d4jules`.
  A estrutura agora é:
  - `scraper_cli.py` (na raiz do projeto)
  - `config/` (para arquivos de configuração)
  - `src/` (diretório principal do código da aplicação)
  - `src/core/` (para lógica principal como analyzer, crawler, parser, writer)
  - `src/utils/` (para funções utilitárias, se necessário)
  - `output/` (para salvar os arquivos Markdown gerados)
  - `logs/` (para logs da aplicação, a ser criado futuramente)
  - `tests/` (para os testes do projeto, com subdiretório `tests/core/` para testes dos módulos core)
  - `docs/` (para documentação adicional do projeto)

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "Estrutura de diretórios original criada. Refatorada posteriormente para remover o diretório 'd4jules' de topo e mover seu conteúdo para a raiz."
# start_time: 2024-07-26T10:40:00Z # Estimado (original)
# end_time: 2024-07-26T10:45:00Z # Estimado (original)
# duration_minutes: 5 # Estimado (original)
# files_modified: # Diretórios e .gitkeep files criados originalmente e depois movidos/reestruturados
#   - src/
#   - src/core/
#   - src/core/.gitkeep
#   - src/utils/
#   - src/utils/.gitkeep
#   - config/
#   - output/
#   - output/.gitkeep
#   - tests/
#   - tests/core/
#   - docs/
#   - docs/.gitkeep
#   - scraper_cli.py
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D01.md (para a lista de diretórios original)
#   - VISION.md (para a estrutura alvo após refatoração)
# execution_details: |
#   Originalmente:
#   - `mkdir -p d4jules/core d4jules/utils d4jules/output tests docs config`
#   - `touch d4jules/core/.gitkeep d4jules/utils/.gitkeep d4jules/output/.gitkeep tests/.gitkeep docs/.gitkeep config/.gitkeep`
#   Posteriormente, todo o conteúdo de `d4jules/` (incluindo `scraper_cli.py`, `src`, `config`, `output`) foi movido para a raiz do projeto e o diretório `d4jules` foi removido.
#   `tests/` agora contém `tests/core/`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* N/A (criação de diretórios na raiz do projeto: `src/`, `config/`, `output/`, `tests/`, `docs/`)

## Critérios de Aceitação
1.  Os diretórios `src/`, `src/core/`, `src/utils/`, `config/`, `output/`, `tests/`, `tests/core/` e `docs/` são criados na raiz do projeto.
2.  O arquivo `scraper_cli.py` existe na raiz do projeto.
3.  Arquivos `.gitkeep` são adicionados a diretórios que podem estar vazios inicialmente (ex: `src/utils/`, `output/`, `docs/`) para garantir o versionamento.

## Observações Adicionais
O diretório `output/` deve ser adicionado ao `.gitignore` posteriormente, se os resultados do scraping não forem para ser versionados.
O diretório `logs/` será criado em uma task futura.
O diretório `config/` conterá `config.ini.template` e um `.gitignore` para `config.ini`.
```
