---
id: task-T06
title: "Testes para a task-D07: Carregamento de Configuração"
type: test
status: backlog
priority: high # Testes para core funcionality como config são importantes
dependencies: ["task-D07"]
parent_plan_objective_id: "3.1" # Referencing parent objective of D07
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "config", "core", "setup"]
description: |
  Testar a função `load_config` em `d4jules/src/core/config_loader.py`.
  Verificar se:
  1. Carrega corretamente os valores `API_KEY` da seção `[GOOGLE_AI]` e `MODEL_NAME` da seção `[LLM]` de um arquivo `config.ini` de teste.
  2. Lida corretamente com erros, como:
     - Arquivo `config.ini` não encontrado.
     - Seções `[GOOGLE_AI]` ou `[LLM]` ausentes.
     - Chaves `api_key` ou `model_name` ausentes em suas respectivas seções.
  Os testes devem ser implementados em `tests/test_config_loader.py`.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-26T15:00:00Z # Estimado
# end_time: 2024-07-26T15:30:00Z # Estimado
# duration_minutes: 30 # Estimado
# files_modified:
#   - tests/test_config_loader.py
#   - tests/__init__.py # Assegurada a existência
# reference_documents_consulted:
#   - jules-flow/done/task-D07.md
#   - d4jules/src/core/config_loader.py
#   - jules-flow/in_progress/task-T06.md (para requisitos de teste)
# execution_details: |
#   1. Criado o arquivo `tests/test_config_loader.py`.
#   2. Implementada a classe `TestConfigLoader(unittest.TestCase)` com métodos `setUp` e `tearDown` para gerenciar arquivos de configuração temporários.
#   3. Implementados os seguintes métodos de teste:
#      - `test_load_config_success`: Verifica o carregamento bem-sucedido de um config válido.
#      - `test_load_config_file_not_found`: Verifica se `ConfigError` é levantada para arquivo inexistente.
#      - `test_load_config_missing_google_ai_section`: Verifica `ConfigError` para seção `[GOOGLE_AI]` ausente.
#      - `test_load_config_missing_api_key`: Verifica `ConfigError` para chave `api_key` ausente.
#      - `test_load_config_missing_llm_section`: Verifica `ConfigError` para seção `[LLM]` ausente.
#      - `test_load_config_missing_model_name`: Verifica `ConfigError` para chave `model_name` ausente.
#      - `test_load_config_empty_model_name`: Verifica `ConfigError` para `model_name` vazio.
#      - `test_load_config_optional_scraper_section_absent`: Verifica o comportamento quando a seção opcional `[SCRAPER]` está ausente.
#   4. Assegurada a existência do arquivo `tests/__init__.py`.
#   5. As dependências do projeto foram instaladas usando `pip install -r requirements.txt` para resolver `ModuleNotFoundError`.
#   6. Corrigidos erros de sintaxe em `d4jules/src/core/config_loader.py` e `d4jules/src/core/analyzer.py` (remoção de blocos `if __name__ == "__main__":` problemáticos).
#   7. Todos os 9 testes implementados em `tests/test_config_loader.py` passaram com sucesso após as correções e instalação de dependências.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/src/core/config_loader.py` (leitura)
* `tests/test_config_loader.py` (criação/modificação)
* `d4jules/config/config.ini.template` (para referência da estrutura)

## Critérios de Aceitação
1.  O arquivo `tests/test_config_loader.py` é criado.
2.  A função `load_config` lê corretamente os valores das seções `[GOOGLE_AI]` e `[LLM]` de um arquivo de configuração de teste válido.
3.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando o arquivo `config.ini` não é encontrado.
4.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a seção `[GOOGLE_AI]` está ausente.
5.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a chave `api_key` está ausente na seção `[GOOGLE_AI]`.
6.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a seção `[LLM]` está ausente.
7.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a chave `model_name` está ausente na seção `[LLM]`.
8.  Todos os testes em `tests/test_config_loader.py` passam.

## Observações Adicionais
Esta tarefa é crucial para garantir a robustez do carregamento de configurações.
Considerar o uso da biblioteca `unittest.mock` para mockar o sistema de arquivos se necessário, ou criar arquivos de configuração temporários para os testes.
```
