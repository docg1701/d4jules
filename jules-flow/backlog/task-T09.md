---
id: task-T09
title: "Testes para a task-D05: Ativação de venv e instalação de dependências em start.sh"
type: test
status: backlog
priority: medium
dependencies: ["task-D05"]
parent_plan_objective_id: "2.2" # Referencing parent objective of D05
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "shell", "automation", "setup"]
description: |
  Testar o script `start.sh` para verificar se ele inclui corretamente os comandos para:
  1. Ativar o ambiente virtual `.venv`.
  2. Executar `git pull` (especificamente `git pull origin $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")`).
  3. Executar `pip install --upgrade pip`.
  4. Instalar dependências de `requirements.txt` usando `pip install -r requirements.txt`.
  Os testes devem verificar a presença desses comandos e a exibição de mensagens de usuário apropriadas.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified: [] # Testes são de execução e verificação de output/estado
# reference_documents_consulted:
#   - jules-flow/done/task-D05.md
#   - start.sh
# execution_details: |
#   1. Ler o conteúdo do script `start.sh`.
#   2. Verificar a presença exata ou funcionalmente equivalente dos seguintes comandos na ordem correta:
#      - `source .venv/bin/activate` (ou `source "$VENV_DIR/bin/activate"`)
#      - `git pull origin $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")` (ou similar que puxe o branch atual)
#      - `pip install --upgrade pip`
#      - `pip install -r requirements.txt`
#   3. Verificar se há `echo` statements antes de cada um desses comandos principais para informar o usuário.
#   4. (Opcional, se possível no ambiente de teste) Executar o script e verificar os códigos de saída (assumindo que mocks/stubs seriam necessários para `git pull` e `pip install` em um ambiente de teste puro sem rede/git). Para esta task, a verificação estática do script pode ser suficiente, dado que a task D05 focou na adição dos comandos.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (leitura e análise)
* `requirements.txt` (referência)

## Critérios de Aceitação
1.  O script `start.sh` contém o comando para ativar o ambiente virtual (ex: `source .venv/bin/activate`).
2.  O script `start.sh` contém o comando para executar `git pull` (preferencialmente `git pull origin $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")`).
3.  O script `start.sh` contém o comando `pip install --upgrade pip`.
4.  O script `start.sh` contém o comando `pip install -r requirements.txt`.
5.  Mensagens informativas para o usuário (via `echo`) estão presentes antes de cada uma dessas ações principais.

## Observações Adicionais
Esta tarefa foca na verificação da presença e ordem correta dos comandos no script. A execução real e seus efeitos (como a instalação de pacotes) foi parcialmente verificada manualmente na task D05 e será mais completamente testada em `task-T01` (Testar script start.sh - que é uma task mais abrangente para o `start.sh` final).
```
