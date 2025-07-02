---
id: task-T01
title: "Testar script start.sh"
type: test
status: backlog
priority: medium
dependencies: ["task-D04", "task-D05", "task-D06", "task-D03"]
parent_plan_objective_id: "Passo2-Test" # Referência ao teste do Passo 2 do working-plan
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["test", "shell", "automation", "setup"]
description: |
  Executar o script `start.sh` para verificar seu comportamento completo.
  O teste deve cobrir:
  1. Criação do ambiente virtual `.venv` se ele não existir.
  2. Ativação bem-sucedida do ambiente virtual.
  3. Tentativa de `git pull` (deve funcionar se o repositório estiver configurado).
  4. Instalação de dependências do `requirements.txt`.
  5. Tentativa de execução do script `python d4jules/scraper_cli.py`.

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
# reference_documents_consulted:
#   - task-D04.md
#   - task-D05.md
#   - task-D06.md
# execution_details: |
#   - Tornar `start.sh` executável (`chmod +x start.sh`).
#   - Executar `./start.sh`.
#   - Verificar a saída para confirmar que:
#     - Mensagem de criação/existência do venv aparece.
#     - `git pull` é tentado.
#     - `pip install` é executado e tenta instalar pacotes de `requirements.txt`.
#     - Há uma tentativa de executar `python d4jules/scraper_cli.py`, que deve falhar
#       com "No such file or directory" ou similar, pois o script ainda não existe.
#     - Nenhum erro de sintaxe do shell ocorre no `start.sh`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (execução)
* `requirements.txt` (leitura pelo `start.sh`)
* Saída do console durante a execução do `start.sh`.

## Critérios de Aceitação
1.  O script `start.sh` é executável.
2.  Se `.venv` não existir, ele é criado. Se existir, o script continua.
3.  O script tenta executar `git pull`.
4.  O script tenta instalar dependências de `requirements.txt` usando `pip` do ambiente virtual.
5.  O script tenta executar `python d4jules/scraper_cli.py`. A falha na execução do `scraper_cli.py` (ex: "file not found") é aceitável e esperada nesta fase, desde que o `start.sh` em si não apresente erros de sintaxe ou lógica.
6.  Não há erros de sintaxe no script `start.sh`.

## Observações Adicionais
Este teste foca no funcionamento correto do `start.sh` em si, não na aplicação Python que ele eventualmente chamará.
```
