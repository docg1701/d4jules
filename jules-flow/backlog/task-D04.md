---
id: task-D04
title: "Desenvolver verificação e criação de .venv em start.sh"
type: development
status: backlog
priority: medium
dependencies: []
parent_plan_objective_id: "2.1"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "shell", "automation", "setup"]
description: |
  No script `start.sh` (a ser criado na raiz do projeto), adicionar lógica para verificar se o diretório de ambiente virtual `.venv` existe na raiz do projeto. Se não existir, o script deve criar um ambiente virtual Python 3 chamado `.venv`.

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
#   - jules_bootstrap.sh (para confirmar disponibilidade de python3-venv)
# execution_details: |
#   Script `start.sh` criado/atualizado com comandos para verificar a existência de `.venv`
#   e criá-lo com `python3 -m venv .venv` caso não exista.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (criação/modificação na raiz do projeto)

## Critérios de Aceitação
1.  O script `start.sh` é criado ou modificado.
2.  O script contém comandos shell para verificar a existência do diretório `.venv`.
3.  Se `.venv` não existir, o script o cria usando `python3 -m venv .venv`.
4.  O script deve ser executável (`chmod +x start.sh`).

## Observações Adicionais
Este é o primeiro passo para o `start.sh`. As demais funcionalidades (ativação, dependências, execução) serão adicionadas em tasks subsequentes.
O `jules_bootstrap.sh` já garante que `python3-venv` está instalado.
```
