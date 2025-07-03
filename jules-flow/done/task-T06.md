---
id: task-T06
title: "Testes para a task-D07: Carregamento de Configuração"
type: test
status: backlog # Will be updated to done in task-index.md
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
  Testar a função `load_config` em `src/core/config_loader.py`. # Corrected path
  Verificar se:
  1. Carrega corretamente os valores `API_KEY` da seção `[GOOGLE_AI]` e `MODEL_NAME` da seção `[LLM]` de um arquivo `config.ini` de teste.
  2. Lida corretamente com erros, como:
     - Arquivo `config.ini` não encontrado.
     - Seções `[GOOGLE_AI]` ou `[LLM]` ausentes.
     - Chaves `api_key` ou `model_name` ausentes em suas respectivas seções.
     - `model_name` vazio.
  Os testes devem ser implementados em `tests/test_config_loader.py`.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: "success"
# outcome_reason: "All tests passed after installing dependencies."
# start_time: "YYYY-MM-DDTHH:MM:SSZ" # Placeholder, actual time not tracked by Jules
# end_time: "YYYY-MM-DDTHH:MM:SSZ" # Placeholder, actual time not tracked by Jules
# duration_minutes: 15 # Estimated
# files_modified:
#   - "tests/__init__.py"
#   - "tests/test_config_loader.py"
# reference_documents_consulted:
#   - "src/core/config_loader.py"
#   - "config/config.ini.template"
#   - "jules-flow/instructions-for-jules.md"
#   - "jules-flow/in_progress/task-T06.md" # For task requirements
# execution_details: |
#   1. Verified the `tests/` directory exists.
#   2. Created `tests/__init__.py` to make `tests` a Python package.
#   3. Created `tests/test_config_loader.py` with a `TestConfigLoader` class inheriting from `unittest.TestCase`.
#   4. Implemented `setUp` and `tearDown` methods to manage temporary configuration files in a `temp_test_config_dir` directory.
#   5. Implemented the following test methods:
#      - `test_load_config_success`: Checks successful loading of API_KEY, MODEL_NAME, scraper_settings, and other generic sections with type conversion.
#      - `test_load_config_file_not_found_with_template`: Checks ConfigError when config file is missing but template exists.
#      - `test_load_config_file_not_found_no_template`: Checks ConfigError when neither config file nor template exists.
#      - `test_load_config_missing_google_ai_section`: Checks ConfigError for missing [GOOGLE_AI] section.
#      - `test_load_config_missing_api_key`: Checks ConfigError for missing api_key in [GOOGLE_AI].
#      - `test_load_config_missing_llm_section`: Checks ConfigError for missing [LLM] section.
#      - `test_load_config_missing_model_name`: Checks ConfigError for missing model_name in [LLM].
#      - `test_load_config_empty_model_name`: Checks ConfigError for empty model_name in [LLM].
#      - `test_load_config_optional_scraper_section_present`: Checks loading when [SCRAPER] section is present.
#      - `test_load_config_optional_scraper_section_absent`: Checks behavior when [SCRAPER] section is absent (should return empty dict for scraper_settings).
#      - `test_load_config_other_sections_conversion`: Checks loading and type conversion for other generic sections.
#   6. Initial test run failed due to `ModuleNotFoundError: No module named 'bs4'`.
#   7. Read `requirements.txt` and installed dependencies using `pip install -r requirements.txt`.
#   8. Re-ran tests using `python -m unittest tests.test_config_loader`. All 11 tests passed.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/config_loader.py` (leitura) # Corrected path
* `tests/test_config_loader.py` (criação/modificação)
* `config/config.ini.template` (para referência da estrutura) # Corrected path

## Critérios de Aceitação
1.  O arquivo `tests/test_config_loader.py` é criado.
2.  A função `load_config` lê corretamente os valores das seções `[GOOGLE_AI]` e `[LLM]` de um arquivo de configuração de teste válido.
3.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando o arquivo `config.ini` não é encontrado.
4.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a seção `[GOOGLE_AI]` está ausente.
5.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a chave `api_key` está ausente na seção `[GOOGLE_AI]`.
6.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a seção `[LLM]` está ausente.
7.  A função `load_config` levanta `ConfigError` (ou uma exceção apropriada) quando a chave `model_name` está ausente na seção `[LLM]`.
8.  A função `load_config` levanta `ConfigError` quando `model_name` está vazio.
9.  Todos os testes em `tests/test_config_loader.py` passam.

## Observações Adicionais
Esta tarefa é crucial para garantir a robustez do carregamento de configurações.
Considerar o uso da biblioteca `unittest.mock` para mockar o sistema de arquivos se necessário, ou criar arquivos de configuração temporários para os testes.
O comportamento da seção `[SCRAPER]` e outras seções genéricas também deve ser testado.
```
