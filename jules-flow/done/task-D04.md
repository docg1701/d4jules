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
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-26T17:00:00Z # Estimado
# end_time: 2024-07-26T17:15:00Z # Estimado
# duration_minutes: 15 # Estimado
# files_modified:
#   - start.sh
#   - .gitignore # Adicionado .venv/
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D04.md
#   - VISION.md
# execution_details: |
#   1. Criado o arquivo `start.sh` na raiz do projeto com o shebang `#!/bin/bash`.
#   2. Implementada a lógica para verificar se o diretório `.venv` existe.
#      - Se não existe, imprime "Virtual environment '.venv' not found. Creating..." e executa `python3 -m venv .venv`. Imprime mensagem de sucesso ou erro.
#      - Se existe, imprime "Virtual environment '.venv' found."
#   3. O script `start.sh` foi tornado executável com `chmod +x start.sh`.
#   4. Adicionado `.venv/` ao arquivo `.gitignore` (criado se não existisse) para evitar que o ambiente virtual seja versionado.
#   5. Testes manuais foram realizados:
#      - Cenário 1 (.venv não existe): `rm -rf .venv`, `./start.sh`. Verificou-se a criação do `.venv` e as mensagens corretas.
#      - Cenário 2 (.venv existe): `./start.sh` novamente. Verificou-se a mensagem de que o venv foi encontrado.
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
