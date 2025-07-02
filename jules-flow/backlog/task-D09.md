---
id: task-D09
title: "Implementar análise de HTML com LLM para extrair seletores"
type: development
status: backlog
priority: high
dependencies: ["task-D07", "task-R01", "task-R02"] # D07 para config, R01/R02 para conhecimento LangChain/Gemini
parent_plan_objective_id: "3.3"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "llm", "langchain", "gemini", "html", "core"]
description: |
  Desenvolver a funcionalidade de análise de HTML usando um modelo de linguagem (LLM) para extrair seletores CSS.
  Esta funcionalidade deve ser encapsulada, preferencialmente em um novo arquivo como `d4jules/core/analyzer.py`.
  A função principal deve:
  1. Aceitar uma URL como entrada.
  2. Baixar o conteúdo HTML da URL usando a biblioteca `requests`.
  3. Preparar um prompt para o LLM, incluindo o HTML baixado (ou uma porção relevante dele, considerando limites de token) e instruções para identificar seletores CSS para:
      a. A área de conteúdo principal da página.
      b. Links de navegação internos do site.
      c. Opcional: Link para a "próxima página" em caso de paginação.
  4. Utilizar LangChain com o modelo Gemini (configurado via `config.ini`) para enviar o prompt.
  5. A resposta do LLM deve ser estruturada (JSON). Utilizar o método `.with_structured_output()` do LangChain, definindo um Pydantic model (ou TypedDict) para o schema esperado (ex: `content_selector: str`, `navigation_selector: str`, `next_page_selector: Optional[str]`).
  6. Processar a resposta JSON para extrair os seletores.
  7. Retornar os seletores extraídos.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified:
#   - d4jules/core/analyzer.py
#   - d4jules/scraper_cli.py (para integrar/chamar o analyzer)
# reference_documents_consulted:
#   - jules-flow/working-plan.md
#   - jules-flow/docs/reference/langchain_research.md
#   - jules-flow/docs/reference/gemini_api_research.md
#   - task-D07.md (para saber como as configs são carregadas)
# execution_details: |
#   Criado `d4jules/core/analyzer.py`.
#   Definido Pydantic model para os seletores.
#   Implementada função `analyze_url_for_selectors(url, config)` que:
#     - Baixa HTML com `requests`.
#     - Instancia `ChatGoogleGenerativeAI` com `model_name` do config.
#     - Usa `.with_structured_output(PydanticModel)` no LLM.
#     - Cria prompt e invoca o LLM estruturado.
#     - Retorna os seletores parseados.
#   Adicionado tratamento de erro para falhas no download ou na chamada LLM.
#   Integrada a chamada ao `analyzer` no `scraper_cli.py`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/core/analyzer.py` (criação)
* `d4jules/scraper_cli.py` (para chamar a função de análise)
* `d4jules/config.ini` (leitura para API key e nome do modelo)

## Critérios de Aceitação
1.  Uma função é criada em `d4jules/core/analyzer.py` que baixa o HTML de uma URL.
2.  A função prepara um prompt adequado para o LLM, instruindo-o a encontrar os seletores CSS.
3.  A função utiliza LangChain e o modelo Gemini (configurado) para processar o prompt.
4.  A resposta do LLM é parseada como JSON (usando `.with_structured_output()`) para extrair `content_selector`, `navigation_selector`, e opcionalmente `next_page_selector`.
5.  A função retorna os seletores de forma estruturada.
6.  A função lida com possíveis erros (ex: falha no download, erro na API do LLM).
7.  Testes unitários para a função de análise (mockando a chamada ao LLM e `requests.get`) são desejáveis.

## Observações Adicionais
Considerar o tamanho do HTML enviado ao LLM. Para páginas muito grandes, pode ser necessário enviar apenas o `<body>` ou uma parte inicial significativa. A qualidade dos seletores dependerá da capacidade do LLM e da clareza do prompt.
```
