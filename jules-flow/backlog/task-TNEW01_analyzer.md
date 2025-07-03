---
id: task-TNEW01_analyzer
title: "Reescrever testes para src/core/analyzer.py"
type: test
status: backlog
priority: high
dependencies: ["task-D09"] # Depends on the analyzer implementation
parent_plan_objective_id: null # To be defined if part of a larger test plan
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "llm", "analyzer", "core"]
description: |
  Reescrever os testes unitários e de integração para o módulo `src/core/analyzer.py`.
  Os testes originais (`tests/test_analyzer.py`) foram apagados devido a instabilidades na ferramenta de execução de testes.

  **Funcionalidades a serem testadas (com base no `tests/test_analyzer.py` original e `task-D09`):**
  1.  **`analyze_url_for_selectors` sucesso:**
      - Mockar `requests.get` para retornar HTML de exemplo.
      - Mockar `ChatGoogleGenerativeAI` e `.with_structured_output()` para retornar um objeto `HtmlSelectors` esperado.
      - Verificar se `requests.get` e os métodos do LLM são chamados corretamente.
      - Verificar se a variável de ambiente `GOOGLE_API_KEY` é configurada.
      - Validar se o resultado é o objeto `HtmlSelectors` esperado.
  2.  **Tratamento de Erros de Rede:**
      - Mockar `requests.get` para levantar `requests.exceptions.RequestException`.
      - Verificar se `NetworkError` é levantada pela função.
  3.  **Tratamento de Erros de Inicialização do LLM:**
      - Mockar `ChatGoogleGenerativeAI` para levantar uma exceção durante a inicialização.
      - Verificar se `LLMAnalysisError` (com mensagem apropriada) é levantada.
  4.  **Tratamento de Erros na Invocação do LLM:**
      - Mockar o método `invoke` do LLM estruturado para levantar uma exceção.
      - Verificar se `LLMAnalysisError` (com mensagem apropriada) é levantada.
  5.  **Tratamento de Tipo de Resposta Incorreta do LLM:**
      - Mockar o método `invoke` para retornar um tipo de objeto inesperado (não `HtmlSelectors`).
      - Verificar se `LLMAnalysisError` (com mensagem apropriada) é levantada.
  6.  **Validação de Configuração:**
      - Testar o comportamento quando `api_key` está ausente na configuração.
      - Testar o comportamento quando `model_name` está ausente na configuração.
      - Verificar se `AnalyzerError` é levantada nesses casos.

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/test_analyzer.py`.
  - Utilizar `unittest` e `unittest.mock`.

## Critérios de Aceitação
- Todos os cenários acima são cobertos por testes.
- Os testes passam consistentemente.
- Mocks são usados efetivamente para isolar a unidade sob teste e simular dependências externas (rede, LLM).
- Os testes verificam não apenas os resultados felizes, mas também o tratamento de erros e casos de borda.
---
