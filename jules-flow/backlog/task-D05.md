---
id: task-D05
title: "Adicionar ativação de venv, git pull e instalação de dependências ao start.sh"
type: development
status: backlog
priority: medium
dependencies: ["task-D03", "task-D04"]
parent_plan_objective_id: "2.2"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "shell", "automation", "setup"]
description: |
  Continuar o desenvolvimento do script `start.sh`. Após a verificação/criação do ambiente virtual (`.venv`), adicionar os seguintes comandos:
  1. Ativar o ambiente virtual (ex: `source .venv/bin/activate`).
  2. Executar `git pull` para garantir que o código está atualizado. (Considerar `git pull origin $(git rev-parse --abbrev-ref HEAD)` para o branch atual).
  3. Instalar/atualizar as dependências listadas em `requirements.txt` usando `pip install -r requirements.txt`.

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
#   Script `start.sh` atualizado para incluir ativação do venv, `git pull` no branch atual,
#   e `pip install -r requirements.txt`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (modificação)
* `requirements.txt` (leitura pelo script)

## Critérios de Aceitação
1.  O script `start.sh` ativa corretamente o ambiente virtual `.venv`.
2.  O script executa `git pull` para o branch atual.
3.  O script instala as dependências do `requirements.txt` usando `pip`.
4.  Os comandos são executados na ordem correta e dentro do ambiente virtual ativado (para `pip install`).

## Observações Adicionais
O comando `git pull` assume que o repositório já está clonado e configurado com um remote `origin`.
```
