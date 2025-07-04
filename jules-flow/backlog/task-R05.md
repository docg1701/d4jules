---
id: task-R05
title: "Refatorar start.sh para Usar 'python -m src.scraper_cli'"
type: refactor
status: backlog
priority: low
dependencies: []
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["build", "execution", "python-best-practice"]
description: |
  Modificar o script `start.sh` para executar a aplicação CLI principal usando o comando `python3 -m src.scraper_cli` em vez de `python3 src/scraper_cli.py`.
  A execução com `-m` é geralmente a forma mais robusta e recomendada para executar módulos de um pacote em Python, pois lida corretamente com o `PYTHONPATH` e os imports relativos.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified: []
# reference_documents_consulted: []
# execution_details: |
#
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh`

## Critérios de Aceitação
1. A linha de execução no `start.sh` é alterada de `python3 src/scraper_cli.py` para `python3 -m src.scraper_cli`.
2. A aplicação CLI continua a iniciar e operar corretamente quando executada através do `start.sh` modificado.
3. Os imports relativos dentro do pacote `src` (ex: em `scraper_cli.py` importando de `.core`) continuam funcionando como esperado.

## Observações Adicionais
Esta é uma pequena refatoração que alinha o script de execução com as melhores práticas do Python para execução de pacotes.
Verificar se o `PYTHONPATH` ou o diretório de trabalho atual (que é a raiz do projeto quando `start.sh` é executado) são suficientes para que `-m src.scraper_cli` encontre o pacote `src`. Geralmente, executar da raiz do projeto onde `src` é um subdiretório funciona bem com `-m`.
