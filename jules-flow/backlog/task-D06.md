---
id: task-D06
title: "Adicionar execução do scraper_cli.py ao start.sh"
type: development
status: backlog
priority: medium
dependencies: ["task-D05"]
parent_plan_objective_id: "2.3"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "shell", "automation"]
description: |
  Finalizar o script `start.sh` adicionando o comando para executar a aplicação principal Python.
  O comando deve ser `python d4jules/scraper_cli.py` (ou o caminho correto, assumindo que `scraper_cli.py` estará dentro do diretório `d4jules`).
  Este comando deve ser o último a ser executado pelo `start.sh` e deve rodar dentro do ambiente virtual ativado.

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
#   - start.sh
# reference_documents_consulted:
#   - jules-flow/working-plan.md
# execution_details: |
#   Script `start.sh` atualizado para incluir o comando `python d4jules/scraper_cli.py`
#   como sua etapa final.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (modificação)

## Critérios de Aceitação
1.  O script `start.sh` contém o comando `python d4jules/scraper_cli.py` como sua última ação principal.
2.  O comando de execução do Python é chamado após a ativação do venv e instalação de dependências.

## Observações Adicionais
O script `d4jules/scraper_cli.py` ainda não existirá quando esta task for implementada, então a execução falhará, o que é esperado nessa fase. O teste `task-T01` validará o comportamento do `start.sh` em si.
```
