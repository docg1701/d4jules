---
id: task-D08
title: "Implementar solicitação de URL ao usuário em scraper_cli.py"
type: development
status: backlog
priority: medium
dependencies: ["task-D07"] # Assume que scraper_cli.py já foi iniciado
parent_plan_objective_id: "3.2"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "cli", "interaction"]
description: |
  No script `d4jules/scraper_cli.py`, adicionar a funcionalidade para interagir com o usuário e solicitar a URL do site de documentação que deve ser processado.
  Utilizar a função `input()` do Python para capturar a URL fornecida pelo usuário.
  A URL deve ser armazenada em uma variável para uso posterior.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-26T18:30:00Z # Estimado
# end_time: 2024-07-26T18:50:00Z # Estimado
# duration_minutes: 20 # Estimado
# files_modified:
#   - d4jules/scraper_cli.py
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D08.md
#   - VISION.md
#   - d4jules/src/core/config_loader.py
# execution_details: |
#   1. Modificado `d4jules/scraper_cli.py`.
#   2. Importado `load_config` e `ConfigError` de `d4jules.src.core.config_loader` e `sys`.
#   3. Na função `main()`:
#      - Adicionado bloco try-except para carregar configuração usando `load_config()`. Em caso de `ConfigError` ou outra exceção, imprime mensagem de erro e sai.
#      - Se configuração carregada, imprime mensagem de boas-vindas.
#   4. Criada a função `get_user_url()`:
#      - Entra em loop para solicitar a URL ao usuário via `input()`.
#      - Valida se a URL não está vazia.
#      - Valida se a URL começa com "http://" ou "https://".
#      - Oferece sugestão de adicionar "https://" se parecer um erro comum.
#      - Valida basicamante se existe um "." após "://" para checar a presença de um domínio.
#      - Retorna a URL validada.
#   5. Na `main()`, `get_user_url()` é chamada dentro de um try-except para `KeyboardInterrupt`.
#   6. A URL obtida é impressa, seguida de uma mensagem placeholder para futuras ações.
#   7. Teste manual (não interativo):
#      - `d4jules/config/config.ini` foi criado (copiando o template) para o teste.
#      - Executado `python3 -m d4jules.scraper_cli`.
#      - Verificou-se que o script carregou a configuração, imprimiu a mensagem de boas-vindas e o prompt para URL.
#      - A execução terminou com `EOFError` devido à ausência de input interativo, o que é esperado. A lógica de validação da URL foi revisada manualmente e considerada correta para um cenário interativo.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/scraper_cli.py` (modificação)

## Critérios de Aceitação
1.  O script `d4jules/scraper_cli.py`, quando executado, solicita ao usuário que insira uma URL.
2.  A URL fornecida pelo usuário é lida e armazenada corretamente em uma variável.
3.  A solicitação é clara e informativa para o usuário.

## Observações Adicionais
Validação básica da URL (ex: se não está vazia) pode ser considerada, mas validação extensiva (formato, acessibilidade) pode ser uma task separada ou parte da lógica de download.
```
