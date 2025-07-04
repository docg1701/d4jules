---
id: task-R03
title: "Melhorar Tratamento de Erros na Orquestração de Scraping"
type: refactor
status: backlog # Original status
priority: medium
dependencies: ["task-R01"]
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["crawler", "error-handling"]
description: |
  Implementar tratamento de erro mais granular no loop de processamento de página dentro do `Crawler` (após a refatoração da task-R01).
  Atualmente, o tratamento de erro no `scraper_cli.py` é muito genérico.
  O `Crawler` deve ser capaz de capturar exceções específicas das fases de análise, parsing e escrita para uma URL individual, registrar o erro e, idealmente, continuar com as próximas URLs.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-04T11:00:00Z # Estimativa
# end_time: 2024-07-04T11:15:00Z # Estimativa
# duration_minutes: 15 # Estimativa
# files_modified:
#   - src/core/crawler.py
# reference_documents_consulted:
#   - src/core/analyzer.py # Para nomes de exceções
# execution_details: |
#   1. Refinado o tratamento de exceções no método `start_crawling` de `src/core/crawler.py`:
#      - Bloco de análise (`analyzer_func`):
#        - Captura específica de `(AnalyzerError, NetworkError, LLMAnalysisError)`.
#        - Captura genérica de `Exception` para outros erros inesperados do analisador.
#        - Adicionada verificação para `selectors is None` como salvaguarda.
#      - Bloco de download de HTML (`requests.get`):
#        - Captura específica para `requests.exceptions.Timeout`.
#        - Captura específica para `requests.exceptions.HTTPError`.
#        - Captura mais genérica `requests.exceptions.RequestException` para outros erros de rede.
#        - Captura genérica de `Exception` para outros erros inesperados.
#        - Adicionada verificação `html_content_for_parser is None` como salvaguarda.
#      - Bloco de parsing (`parser_func`):
#        - Mantida a captura genérica de `Exception`, pois as exceções de BeautifulSoup podem ser variadas.
#        - Adicionada verificação `if not self.parser_func:` (deveria ser pega no init, mas é defensivo).
#      - Bloco de escrita (`writer_func`):
#        - Captura específica para `IOError`.
#        - Captura genérica de `Exception` para outros erros inesperados do writer.
#        - Adicionada verificação `if not self.writer_func:` (deveria ser pega no init).
#   2. Em todos os casos de erro durante o processamento de uma página, uma mensagem de erro é impressa (futuramente logada) e o crawler continua para a próxima URL (`continue`).
#   3. As mensagens de erro agora incluem `type(e).__name__` para clareza sobre o tipo de exceção.
#   4. Nenhuma alteração nos testes foi estritamente necessária, pois os testes de `task-R01` já cobriam o comportamento de "continuar em erro". Apenas foi verificado se eles ainda passavam.
#
# O tratamento de erros no crawler está mais robusto e específico.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/crawler.py`
* `src/scraper_cli.py` (para possível ajuste na forma como os erros do crawler são reportados/logados)
* `src/core/analyzer.py` (para referência das exceções: `AnalyzerError`, `NetworkError`, `LLMAnalysisError`)
* `src/core/writer.py` (para referência a `IOError` ou exceções customizadas se adicionadas)

## Critérios de Aceitação
1. Dentro do loop de processamento de página do `Crawler.start_crawling()`:
    a. As chamadas para os componentes de análise, parsing e escrita são envolvidas em blocos `try-except`.
    b. Exceções específicas como `AnalyzerError`, `NetworkError`, `LLMAnalysisError` (do analyzer), e possíveis erros de parsing ou `IOError` (do writer) são capturadas.
2. Quando um erro ocorre para uma página específica, o erro é registrado (inicialmente via `print` ou, se a task-R04 estiver concluída, via `logging`).
3. O `Crawler` continua o processamento com a próxima URL na fila, em vez de parar toda a execução (a menos que seja um erro catastrófico configurado para parar).
4. O `scraper_cli.py` pode opcionalmente reportar um resumo de erros ao final da execução.

## Observações Adicionais
A estratégia de "continuar em erro" é geralmente preferível para um crawler, para maximizar a quantidade de conteúdo recuperado.
Pode-se considerar um contador de erros ou uma lista de URLs que falharam para relatório final.
