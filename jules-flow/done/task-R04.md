---
id: task-R04
title: "Implementar Logging Estruturado em toda a Aplicação"
type: refactor
status: backlog # Original status
priority: low
dependencies: ["task-R01"] # Melhor aplicar após a lógica principal estar estável
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["logging", "infrastructure"]
description: |
  Substituir as chamadas `print()` existentes por um sistema de logging mais robusto e configurável, utilizando o módulo `logging` padrão do Python.
  Isso permitirá melhor controle sobre a verbosidade da saída, formato dos logs e destino (console, arquivo, etc.).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
outcome: success
outcome_reason: "Structured logging implemented using Python's standard logging module."
start_time: YYYY-MM-DDTHH:MM:SSZ # Placeholder
end_time: YYYY-MM-DDTHH:MM:SSZ # Placeholder
duration_minutes: 0 # Placeholder
files_modified: [
  "src/core/logging_config.py",
  "src/scraper_cli.py",
  "src/core/crawler.py",
  "src/core/writer.py"
]
reference_documents_consulted: ["jules-flow/in_progress/task-R04.md"]
execution_details: |
  - Created `src/core/logging_config.py` to centralize logging setup.
  - Modified `src/scraper_cli.py` to use `setup_logging` and replaced print statements with logger calls.
  - Modified `src/core/crawler.py` to replace print statements with logger calls.
  - Added logger instantiation in `src/core/writer.py` (it already used logger calls but was missing the import and instantiation).
  - `src/core/analyzer.py` and `src/core/config_loader.py` were checked and already conformed or did not require direct logging.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/scraper_cli.py` (para configuração inicial do logger)
* `src/core/crawler.py`
* `src/core/analyzer.py`
* `src/core/parser.py`
* `src/core/writer.py`
* Potencialmente `src/core/config_loader.py` se houver prints lá.

## Critérios de Aceitação
1. Um logger raiz é configurado no `scraper_cli.py` (ou um módulo de utilidades de logging, se criado). A configuração deve definir um formato de log padrão (ex: incluindo timestamp, nível, nome do módulo, mensagem) e um handler inicial (ex: `StreamHandler` para console).
2. Todos os módulos (`crawler`, `analyzer`, `parser`, `writer`, etc.) obtêm suas próprias instâncias de logger usando `logger = logging.getLogger(__name__)`.
3. As chamadas `print()` usadas para informação de progresso, depuração ou erros são substituídas por chamadas apropriadas ao logger (ex: `logger.info()`, `logger.debug()`, `logger.warning()`, `logger.error()`, `logger.exception()` para erros com stack trace).
4. O nível de logging pode ser controlado (ex: através de uma variável de ambiente ou um parâmetro de configuração no futuro, mas inicialmente pode ser fixo em INFO ou DEBUG).
5. O output da aplicação é mais estruturado e informativo devido ao logging.

## Observações Adicionais
Esta refatoração melhora significativamente a manutenibilidade e a capacidade de diagnóstico da aplicação.
Considerar se os logs devem ir para um arquivo além do console. Inicialmente, console é suficiente.
