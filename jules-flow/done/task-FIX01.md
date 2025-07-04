---
id: task-FIX01
title: "Corrigir/Completar Exportações em src/core/__init__.py"
type: fix
status: backlog # Original status
priority: low
dependencies: []
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["core", "module-structure"]
description: |
  O arquivo `src/core/__init__.py` atualmente não exporta todos os componentes necessários do submódulo `analyzer`.
  Especificamente, `analyze_url_for_selectors` e as exceções customizadas (`AnalyzerError`, `NetworkError`, `LLMAnalysisError`) não estão incluídos na lista `__all__` nem são importados diretamente no `__init__.py` para re-exportação.
  Isso força importações mais longas (ex: `from src.core.analyzer import analyze_url_for_selectors`) em vez de permitir `from src.core import analyze_url_for_selectors`.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-04T11:15:00Z # Estimativa
# end_time: 2024-07-04T11:20:00Z # Estimativa
# duration_minutes: 5 # Estimativa
# files_modified:
#   - src/core/__init__.py
# reference_documents_consulted:
#   - src/core/analyzer.py # Para confirmar os nomes dos símbolos
# execution_details: |
#   1. Modificado `src/core/__init__.py`:
#      - Adicionadas as seguintes importações de `.analyzer`:
#        - `analyze_url_for_selectors`
#        - `HtmlSelectors`
#        - `AnalyzerError`
#        - `NetworkError`
#        - `LLMAnalysisError`
#      - Esses nomes foram adicionados à lista `__all__`.
#   2. Verificado que, após a alteração, seria teoricamente possível importar esses símbolos diretamente de `src.core` (ex: `from src.core import analyze_url_for_selectors`).
#   3. A aplicação não foi executada para confirmar, mas a alteração é apenas na exportação de símbolos e não deve quebrar a funcionalidade existente, assumindo que as importações anteriores diretas de `src.core.analyzer` ainda funcionam ou são atualizadas se necessário (o que não é o caso atualmente, pois `scraper_cli.py` já importa `analyze_url_for_selectors` diretamente do submódulo).
#
# A interface do pacote `src.core` foi melhorada.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/__init__.py`
* `src/core/analyzer.py` (para verificar os nomes exatos dos símbolos a serem exportados)

## Critérios de Aceitação
1. O arquivo `src/core/__init__.py` é modificado para importar `analyze_url_for_selectors`, `AnalyzerError`, `NetworkError`, e `LLMAnalysisError` do `src.core.analyzer`.
2. Esses nomes são adicionados à lista `__all__` em `src/core/__init__.py`.
3. Após a modificação, deve ser possível importar esses símbolos diretamente do pacote `src.core`. Por exemplo:
   `from src.core import analyze_url_for_selectors, AnalyzerError`
   deve funcionar sem erros.
4. A aplicação continua a funcionar corretamente após esta alteração.

## Observações Adicionais
Esta é uma correção pequena que melhora a interface do pacote `src.core` e a conveniência de importação para outros módulos.
