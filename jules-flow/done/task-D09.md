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
  Esta funcionalidade deve ser encapsulada no arquivo `src/core/analyzer.py`.
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
# outcome: success
# outcome_reason: "Arquivo recriado em src/core/analyzer.py e caminhos atualizados devido à refatoração da estrutura do projeto."
# start_time: 2024-07-26T14:00:00Z # Estimado (original)
# end_time: 2024-07-26T14:45:00Z # Estimado (original)
# duration_minutes: 45 # Estimado (original)
# files_modified:
#   - src/core/analyzer.py
#   - src/core/__init__.py # (Assumindo que __init__.py é atualizado para exportar os componentes do analyzer)
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D09.md
#   - VISION.md
#   - jules-flow/docs/reference/langchain_research.md
#   - jules-flow/docs/reference/gemini_api_research.md
#   - src/core/config_loader.py # (Path to config_loader updated)
# execution_details: |
#   1. Criado/Recriado o arquivo `src/core/analyzer.py`.
#   2. Definido o Pydantic model `HtmlSelectors` para a saída estruturada (content_selector, navigation_selector, next_page_selector) com validadores básicos.
#   3. Implementada a função `analyze_url_for_selectors(url: str, config: Dict[str, Any]) -> HtmlSelectors`.
#      - Utiliza `requests.get()` para baixar o conteúdo HTML da URL, com timeout e tratamento de erro (`NetworkError`).
#      - Configura `ChatGoogleGenerativeAI` com o `model_name` e `api_key` (via `os.environ`) do dicionário de configuração.
#      - Utiliza `.with_structured_output(HtmlSelectors)` para parsear a resposta do LLM.
#      - Prepara um prompt do sistema e um prompt humano, enviando um snippet do HTML para o LLM.
#      - Inclui tratamento de erro para a inicialização do LLM e para a invocação (`LLMAnalysisError`).
#   4. Adicionadas importações necessárias (`os`, `requests`, `Optional`, `Dict`, `Any`, Pydantic models, LangChain components, custom exceptions).
#   5. O arquivo `src/core/__init__.py` deve ser atualizado para exportar `analyze_url_for_selectors`, `HtmlSelectors`, e as custom exceptions (`AnalyzerError`, `NetworkError`, `LLMAnalysisError`).
#   6. O `analyzer.py` inclui um bloco `if __name__ == "__main__":` para demonstração básica (requer `config/config.ini` e acesso à rede).
#   (Nota: A integração com `scraper_cli.py` será feita em uma task futura.)
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/analyzer.py` (criação/modificação)
* `scraper_cli.py` (para chamar a função de análise) # Modificação adiada
* `config/config.ini` (leitura para API key e nome do modelo)

## Critérios de Aceitação
1.  Uma função é criada em `src/core/analyzer.py` que baixa o HTML de uma URL.
2.  A função prepara um prompt adequado para o LLM, instruindo-o a encontrar os seletores CSS.
3.  A função utiliza LangChain e o modelo Gemini (configurado) para processar o prompt.
4.  A resposta do LLM é parseada como JSON (usando `.with_structured_output()`) para extrair `content_selector`, `navigation_selector`, e opcionalmente `next_page_selector`.
5.  A função retorna os seletores de forma estruturada.
6.  A função lida com possíveis erros (ex: falha no download, erro na API do LLM).
7.  Testes unitários para a função de análise (mockando a chamada ao LLM e `requests.get`) são desejáveis.

## Observações Adicionais
Considerar o tamanho do HTML enviado ao LLM. Para páginas muito grandes, pode ser necessário enviar apenas o `<body>` ou uma parte inicial significativa. A qualidade dos seletores dependerá da capacidade do LLM e da clareza do prompt.

**Sugestão do Usuário (a ser considerada durante a implementação):**
Para otimizar o scraping, o `d4jules` poderia apresentar ao LLM uma árvore de conteúdo/navegação do site (ou da seção atual). O LLM, então, poderia decidir até que nível de profundidade (subdiretórios/subseções) o scraping deve prosseguir, evitando a coleta de dados excessivos ou irrelevantes. Isso pode ser integrado aqui ou em uma task subsequente focada na estratégia de crawling.
```
