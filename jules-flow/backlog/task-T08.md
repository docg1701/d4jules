---
id: task-T08
title: "Testes para a task-D04: Verificação e criação de .venv em start.sh"
type: test
status: backlog
priority: medium
dependencies: ["task-D04"]
parent_plan_objective_id: "2.1" # Referencing parent objective of D04
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "shell", "automation", "setup"]
description: |
  Testar o script `start.sh` para verificar sua funcionalidade de gerenciamento do ambiente virtual `.venv`.
  Especificamente, o teste deve cobrir:
  1. Criação do `.venv` se ele não existir.
  2. Reconhecimento do `.venv` se ele já existir (sem tentativa de recriação).
  3. Exibição de mensagens apropriadas para o usuário em ambos os cenários.

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
#   - jules-flow/done/task-D04.md
#   - start.sh
# execution_details: |
#   1. **Cenário 1: .venv não existe**
#      - `rm -rf .venv` (para garantir que não existe)
#      - Executar `./start.sh`
#      - Verificar a saída do console para as mensagens "Virtual environment '.venv' not found. Creating..." e "Virtual environment '.venv' created successfully.".
#      - Verificar se o diretório `.venv` foi de fato criado (ex: `ls -d .venv`).
#   2. **Cenário 2: .venv existe**
#      - Executar `./start.sh` novamente (sem remover o .venv criado no passo anterior).
#      - Verificar a saída do console para a mensagem "Virtual environment '.venv' found.".
#      - Verificar se o script não tentou recriar o venv (ex: timestamps do diretório .venv não devem mudar significativamente, ou verificar se não há mensagens de erro de recriação).
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (execução)

## Critérios de Aceitação
1.  Quando o diretório `.venv` não existe, a execução de `start.sh` resulta na criação do diretório `.venv`.
2.  Quando o diretório `.venv` não existe, `start.sh` exibe mensagens indicando que o venv não foi encontrado e está sendo criado, seguido de uma mensagem de sucesso.
3.  Quando o diretório `.venv` já existe, a execução de `start.sh` não tenta recriá-lo ou modificá-lo de forma destrutiva.
4.  Quando o diretório `.venv` já existe, `start.sh` exibe uma mensagem indicando que o venv foi encontrado.

## Observações Adicionais
Esta tarefa testa a primeira parte da funcionalidade do `start.sh`. Os testes são baseados na execução do script e observação do seu output e efeitos no sistema de arquivos.
```
