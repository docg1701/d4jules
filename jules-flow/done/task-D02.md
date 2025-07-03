---
id: task-D02
title: "Implementar config.ini para d4jules"
type: development
status: backlog
priority: high
dependencies: ["task-D01"]
parent_plan_objective_id: "1.2"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "config"]
description: |
  Criar o arquivo `config/config.ini.template` (e `config/.gitignore` para `config.ini`) com as seções e campos necessários para configurar a API do Google AI e o modelo LLM a ser utilizado.
  O arquivo `config.ini.template` deve conter:
  Seção `[GOOGLE_AI]` com a chave `api_key = SEU_GOOGLE_API_KEY_AQUI`
  Seção `[LLM]` com a chave `model_name = gemini-1.5-flash-latest`

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "Paths atualizados para refletir a estrutura de diretório refatorada (config/ na raiz)."
# start_time: 2024-07-26T11:30:00Z # Estimado (original)
# end_time: 2024-07-26T11:35:00Z # Estimado (original)
# duration_minutes: 5 # Estimado (original)
# files_modified:
#   - config/config.ini.template
#   - config/.gitignore
#   - config/ # Diretório criado na raiz
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D02.md (descrição da tarefa)
#   - VISION.md (para a estrutura alvo)
# execution_details: |
#   1. Criado o diretório `config/` na raiz do projeto.
#   2. Criado o arquivo `config/config.ini.template` com as seções [GOOGLE_AI] (com API_KEY placeholder) e [LLM] (com MODEL_NAME = gemini-1.5-flash-latest), e uma seção [SCRAPER] como placeholder.
#   3. Criado o arquivo `config/.gitignore` com a entrada `config.ini` para evitar o commit do arquivo de configuração real.
#   4. A criação dos arquivos e do diretório foi verificada.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `config/config.ini.template` (criação)
* `config/config.ini` (ignorado pelo .gitignore, a ser criado pelo usuário)
* `config/.gitignore` (criação)

## Critérios de Aceitação
1.  O arquivo `config/config.ini.template` é criado no diretório `config/`.
2.  O arquivo `config/config.ini.template` contém a seção `[GOOGLE_AI]` com a chave `api_key` e um valor placeholder.
3.  O arquivo `config/config.ini.template` contém a seção `[LLM]` com a chave `model_name` e o valor `gemini-1.5-flash-latest`.
4.  O arquivo `config/.gitignore` é criado e ignora `config.ini`.

## Observações Adicionais
O valor real da `api_key` não deve ser commitado. Instruções sobre como preenchê-lo serão fornecidas no `README.md`.
```
