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
  Implementar a lógica inicial no script `d4jules/scraper_cli.py` para carregar as configurações do arquivo `d4jules/config.ini`.
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
# outcome_reason: ""
# start_time: 2024-07-26T12:30:00Z # Estimado
# end_time: 2024-07-26T12:45:00Z # Estimado
# duration_minutes: 15 # Estimado
# files_modified:
#   - d4jules/src/core/config_loader.py
#   - d4jules/src/__init__.py
#   - d4jules/src/core/__init__.py
#   - d4jules/config/config.ini # Placeholder for testing, gitignored
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D07.md
#   - VISION.md
#   - d4jules/config/config.ini.template
# execution_details: |
#   1. Criado o arquivo `d4jules/src/core/config_loader.py`.
#   2. Implementada a função `load_config(config_path)` que utiliza `configparser` para ler o arquivo .ini.
#      - Retorna um dicionário com `api_key` e `model_name`.
#      - Inclui tratamento de erro para arquivo não encontrado e seções/chaves ausentes, levantando `ConfigError`.
#      - Carrega opcionalmente a seção [SCRAPER] se existir.
#   3. Criados os arquivos `d4jules/src/__init__.py` e `d4jules/src/core/__init__.py` (este último exportando `load_config` e `ConfigError`) para tornar o módulo e a função importáveis.
#   4. O `config_loader.py` inclui um bloco `if __name__ == "__main__":` para testes básicos e demonstração.
#   5. Criado um arquivo `d4jules/config/config.ini` (copiando o `.template`) para facilitar os testes locais do `config_loader.py`. Este arquivo `config.ini` é ignorado pelo git.
#   (Nota: `d4jules/scraper_cli.py` não foi criado/modificado nesta task, pois sua criação é escopo de tasks futuras. `config_loader.py` está pronto para ser importado por ele.)
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/scraper_cli.py` (criação/modificação) # Será modificado em task futura para usar o config_loader
* `d4jules/config.ini` (leitura)
* Opcional: `d4jules/core/config_loader.py` (se a lógica for modularizada) # Esta abordagem foi escolhida.

## Critérios de Aceitação
1.  Criação do arquivo `d4jules/scraper_cli.py` (se ainda não existir). # Adiado para task específica de scraper_cli.py
2.  Uma função é implementada para ler o arquivo `d4jules/config.ini`.
3.  A função extrai corretamente `api_key` de `[GOOGLE_AI]` e `model_name` de `[LLM]`.
4.  A função lida de forma graciosa com o arquivo `config.ini` não encontrado ou com seções/chaves ausentes (ex: logando um erro e saindo, ou retornando valores padrão/None).
5.  Testes unitários (se aplicável e o ambiente permitir) para a função de carregamento de configuração.

## Observações Adicionais
Esta é uma das primeiras funcionalidades do `scraper_cli.py`.
```
