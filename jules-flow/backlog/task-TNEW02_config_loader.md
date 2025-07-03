---
id: task-TNEW02_config_loader
title: "Reescrever testes para src/core/config_loader.py"
type: test
status: backlog
priority: high
dependencies: ["task-D07"] # Depends on the config_loader implementation
parent_plan_objective_id: null
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "config", "core"]
description: |
  Reescrever os testes unitários para o módulo `src/core/config_loader.py`.
  Os testes originais (`tests/test_config_loader.py`) foram apagados.

  **Funcionalidades a serem testadas (com base no `tests/test_config_loader.py` original e `task-D07`):**
  1.  **Carregamento bem-sucedido:**
      - Usar um arquivo `config.ini` temporário com conteúdo válido.
      - Verificar se `load_config` retorna o dicionário esperado com `api_key`, `model_name` e outras seções (ex: `scraper_settings`, `crawler_limits`) devidamente processadas (incluindo conversão de tipo para números).
  2.  **Arquivo não encontrado:**
      - Tentar carregar um caminho de configuração inexistente.
      - Verificar se `ConfigError` é levantada com mensagem apropriada (incluindo menção ao arquivo `.template` se existir).
  3.  **Seções/Chaves Ausentes:**
      - Testar com arquivos de configuração temporários faltando:
          - Seção `[GOOGLE_AI]`
          - Chave `api_key` em `[GOOGLE_AI]`
          - Seção `[LLM]`
          - Chave `model_name` em `[LLM]`
          - Valor para `model_name` (chave existe, mas valor está vazio)
      - Verificar se `ConfigError` é levantada com mensagens apropriadas para cada caso.
  4.  **Seções Opcionais:**
      - Testar com e sem seções opcionais (como `[SCRAPER]`, `[CRAWLER_LIMITS]`) para garantir que são carregadas corretamente se presentes e ignoradas sem erro se ausentes (resultando em dicionários vazios ou valores padrão, conforme a lógica de `load_config`).

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/test_config_loader.py`.
  - Utilizar `unittest`.
  - Usar `setUp` e `tearDown` para criar e remover arquivos de configuração temporários e diretórios.

## Critérios de Aceitação
- Todos os cenários de carregamento de configuração (sucesso e falha) são cobertos.
- Os testes passam consistentemente.
- O tratamento de erros e a robustez do `load_config` são validados.
---
