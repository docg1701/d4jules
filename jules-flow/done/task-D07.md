---
id: task-D07
title: "Implementar carregamento de config.ini em scraper_cli.py"
type: development
status: backlog
priority: high
dependencies: ["task-D01", "task-D02"] # D01 cria d4jules/, D02 cria config.ini
parent_plan_objective_id: "3.1"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "config", "core"]
description: |
  Implementar a lógica inicial no script `scraper_cli.py` (localizado na raiz) para carregar as configurações do arquivo `config/config.ini`.
  A lógica de carregamento reside em `src/core/config_loader.py`.
  Utilizar a biblioteca `configparser` do Python.
  A função de carregamento deve ler:
  - `api_key` da seção `[GOOGLE_AI]`.
  - `model_name` da seção `[LLM]`.
  Esses valores devem ser armazenados de forma acessível para o restante da aplicação.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "Paths atualizados para refletir a estrutura de diretório refatorada (scraper_cli.py na raiz, config_loader.py em src/core/, config.ini em config/)."
# start_time: 2024-07-26T12:30:00Z # Estimado (original)
# end_time: 2024-07-26T12:45:00Z # Estimado (original)
# duration_minutes: 15 # Estimado (original)
# files_modified:
#   - src/core/config_loader.py
#   - src/__init__.py
#   - src/core/__init__.py
#   - config/config.ini # Placeholder for testing, gitignored
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D07.md
#   - VISION.md
#   - config/config.ini.template
# execution_details: |
#   1. Criado o arquivo `src/core/config_loader.py`.
#   2. Implementada a função `load_config(config_path)` que utiliza `configparser` para ler o arquivo .ini.
#      - O caminho padrão para `config_path` foi atualizado para `config/config.ini`.
#      - Retorna um dicionário com `api_key` e `model_name`.
#      - Inclui tratamento de erro para arquivo não encontrado e seções/chaves ausentes, levantando `ConfigError`.
#      - Carrega opcionalmente a seção [SCRAPER] se existir.
#   3. Criados os arquivos `src/__init__.py` e `src/core/__init__.py` (este último exportando `load_config` e `ConfigError`) para tornar o módulo e a função importáveis.
#   4. O `config_loader.py` inclui um bloco `if __name__ == "__main__":` para testes básicos e demonstração.
#   5. Criado um arquivo `config/config.ini` (copiando o `.template`) para facilitar os testes locais do `config_loader.py`. Este arquivo `config.ini` é ignorado pelo git.
#   (Nota: `scraper_cli.py` não foi criado/modificado nesta task para *usar* o config_loader, apenas o config_loader foi preparado. scraper_cli.py já existia e foi movido para a raiz.)
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `scraper_cli.py` (localizado na raiz, será modificado em task futura para usar o config_loader)
* `config/config.ini` (leitura)
* `src/core/config_loader.py` (onde a lógica de carregamento reside)

## Critérios de Aceitação
1.  O arquivo `scraper_cli.py` existe na raiz do projeto.
2.  Uma função é implementada em `src/core/config_loader.py` para ler o arquivo `config/config.ini`.
3.  A função extrai corretamente `api_key` de `[GOOGLE_AI]` e `model_name` de `[LLM]`.
4.  A função lida de forma graciosa com o arquivo `config.ini` não encontrado ou com seções/chaves ausentes.
5.  Testes unitários (se aplicável e o ambiente permitir) para a função de carregamento de configuração.

## Observações Adicionais
A funcionalidade de carregamento de configuração está em `src/core/config_loader.py` e `scraper_cli.py` (na raiz) a utilizará.
```
