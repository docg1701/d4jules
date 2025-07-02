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
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-26T17:30:00Z # Estimado
# end_time: 2024-07-26T17:45:00Z # Estimado
# duration_minutes: 15 # Estimado
# files_modified:
#   - start.sh
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D05.md
#   - VISION.md
#   - requirements.txt
# execution_details: |
#   1. Modificado o script `start.sh` para adicionar os seguintes blocos após a verificação/criação do `.venv`:
#      - Ativação do ambiente virtual: `source .venv/bin/activate`, com verificação de sucesso.
#      - Atualização do repositório: `echo "Updating repository..."` seguido de `git pull origin $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")`, com tratamento de aviso para falhas.
#      - Upgrade do pip: `echo "Upgrading pip..."` seguido de `pip install --upgrade pip`, com tratamento de aviso.
#      - Instalação de dependências: `echo "Installing/updating dependencies from requirements.txt..."` seguido de `pip install -r requirements.txt`, com saída do script em caso de erro.
#   2. Mensagens apropriadas foram adicionadas para cada etapa.
#   3. Testes manuais foram realizados:
#      - `rm -rf .venv` e depois `./start.sh`: Verificou-se a criação do venv, ativação, git pull, upgrade do pip e instalação de dependências.
#      - `./start.sh` novamente: Verificou-se que o venv existente foi encontrado e as etapas subsequentes foram executadas.
#   4. O problema anterior com `.venv/bin/activate` não sendo encontrado foi resolvido, pois a criação e ativação agora ocorrem em uma sequência mais robusta dentro do próprio `start.sh`.
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
