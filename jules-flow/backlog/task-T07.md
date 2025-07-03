---
id: task-T07
title: "Testes para a task-D09: Análise de HTML com LLM para Extração de Seletores"
type: test
status: backlog
priority: high # Core functionality
dependencies: ["task-D09"]
parent_plan_objective_id: "3.3" # Referencing parent objective of D09
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder
tags: ["test", "llm", "analyzer", "core"]
description: |
  Testar a função `analyze_url_for_selectors` no módulo `d4jules/src/core/analyzer.py`.
  Os testes devem cobrir:
  1. Download de HTML (mockando `requests.get`).
  2. Interação com o LLM (mockando `ChatGoogleGenerativeAI` e seu método `invoke` ou o objeto retornado por `with_structured_output`).
  3. Extração correta dos seletores a partir de uma resposta mockada do LLM.
  4. Tratamento de erro para falhas no download de HTML (ex: `requests.exceptions.RequestException`).
  5. Tratamento de erro para falhas na API do LLM (ex: simular um erro na invocação do LLM).
  6. Tratamento de erro para respostas malformadas do LLM (que não se adequam ao Pydantic model `HtmlSelectors`).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-26T16:00:00Z # Estimado
# end_time: 2024-07-26T16:30:00Z # Estimado
# duration_minutes: 30 # Estimado
# files_modified:
#   - tests/test_analyzer.py
# reference_documents_consulted:
#   - jules-flow/done/task-D09.md
#   - d4jules/src/core/analyzer.py
#   - jules-flow/in_progress/task-T07.md (para requisitos de teste)
# execution_details: |
#   1. Criado o arquivo `tests/test_analyzer.py`.
#   2. Implementada a classe `TestAnalyzer(unittest.TestCase)` com um método `setUp` para configurações de teste comuns.
#   3. Implementados os seguintes métodos de teste usando `unittest.mock.patch` para `requests.get` e `langchain_google_genai.ChatGoogleGenerativeAI`:
#      - `test_analyze_url_success`: Verifica o comportamento de sucesso, mockando `requests.get` e a cadeia de chamadas do LLM para retornar um objeto `HtmlSelectors` esperado.
#      - `test_analyze_url_network_error`: Verifica se `NetworkError` é levantada quando `requests.get` falha.
#      - `test_analyze_url_llm_init_error`: Verifica se `LLMAnalysisError` é levantada quando a inicialização de `ChatGoogleGenerativeAI` falha.
#      - `test_analyze_url_llm_invoke_error`: Verifica se `LLMAnalysisError` é levantada quando o método `invoke` do LLM (ou do objeto `structured_llm`) falha.
#      - `test_analyze_url_llm_bad_response_type`: Verifica se `LLMAnalysisError` é levantada quando o LLM retorna um tipo de objeto inesperado.
#      - `test_missing_api_key_in_config`: Verifica se `AnalyzerError` é levantada quando a `api_key` está ausente na configuração.
#      - `test_missing_model_name_in_config`: Verifica se `AnalyzerError` é levantada quando o `model_name` está ausente na configuração.
#   4. Todos os 7 testes implementados passaram com sucesso.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/src/core/analyzer.py` (leitura)
* `tests/test_analyzer.py` (criação/modificação)
* `tests/__init__.py` (criação, se não existir) # Já existe

## Critérios de Aceitação
1.  O arquivo `tests/test_analyzer.py` é criado.
2.  Testes unitários verificam que a função `analyze_url_for_selectors` chama `requests.get` com a URL correta.
3.  Testes unitários verificam que a função formata o prompt para o LLM adequadamente (inspeção do prompt enviado ao mock do LLM).
4.  Testes unitários verificam que a função invoca o LLM (mockado) e processa corretamente uma resposta mockada bem-sucedida, retornando um objeto `HtmlSelectors`.
5.  Testes unitários verificam que a função levanta `NetworkError` quando `requests.get` falha.
6.  Testes unitários verificam que a função levanta `LLMAnalysisError` quando a chamada ao LLM (mockada) falha ou retorna dados inválidos/malformados.
7.  Todos os testes em `tests/test_analyzer.py` passam.

## Observações Adicionais
Será necessário usar `unittest.mock.patch` para mockar `requests.get` e as interações com `ChatGoogleGenerativeAI`.
Considerar a criação de arquivos HTML de teste simples para serem retornados pelo `requests.get` mockado.
```
