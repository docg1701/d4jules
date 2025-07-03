---
id: task-TNEW06_crawler_integration
title: "Reescrever testes de integração para src/core/crawler.py"
type: test
status: backlog
priority: high
dependencies: ["task-D10", "task-FIX01", "task-TNEW01_analyzer", "task-TNEW03_parser", "task-TNEW04_writer"] # Depends on crawler and its mocked dependencies
parent_plan_objective_id: null
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "crawler", "integration-test", "core", "mocking"]
description: |
  Reescrever os testes de integração para a classe `Crawler` em `src/core/crawler.py`.
  Estes testes verificam o fluxo de crawling de ponta a ponta, mockando as dependências externas como `analyzer`, `requests`, `parser` e `writer`.
  Os testes originais (`tests/core/test_crawler_integration.py`) foram apagados.

  **Funcionalidades a serem testadas (com base no `tests/core/test_crawler_integration.py` original):**
  O foco principal é o método `start_crawling()` e sua interação com os componentes mockados.
  1.  **Inicialização do Crawler para Testes:**
      - `setUp` deve mockar `analyzer_patch_path = 'src.core.crawler.analyzer'`, `requests_patch_path = 'src.core.crawler.requests.get'`, etc.
      - Configurar comportamentos padrão para os mocks (ex: `mock_analyzer.analyze_url_for_selectors.return_value`, `mock_requests_get.return_value`).
      - `tearDown` deve parar todos os patchers.
  2.  **Crawling de Página Única:**
      - Configurar o mock do `parser` para não retornar novos links.
      - Verificar se `analyze_url_for_selectors`, `requests.get`, `parse_html_content`, e `save_content_as_markdown` são chamados uma vez com os argumentos corretos.
      - Verificar contagem de páginas processadas e URLs visitadas.
  3.  **Seguimento de Links e Limite de Páginas (`max_pages`):**
      - Configurar o mock do `parser` com `side_effect` para simular a descoberta de links.
      - Verificar se o crawler segue os links e para quando `max_pages` é atingido.
      - Validar o número de chamadas para os componentes mockados.
  4.  **Respeito à Profundidade Máxima (`max_depth`):**
      - Configurar o mock do `parser` para descobrir links em diferentes profundidades.
      - Verificar se o crawler não processa páginas além da `max_depth`.
      - Validar quais URLs foram visitadas e quais não foram.
  5.  **Tratamento de Erros nos Componentes:**
      - Simular falha no `analyzer` (retornar `None`): verificar se o processamento da página para ali.
      - Simular falha no `requests.get` (levantar `requests.exceptions.RequestException`): verificar se o parser não é chamado.
      - Simular falha no `parser` (levantar `Exception`): verificar se o writer não é chamado.
      - Simular falha no `writer` (retornar `None`): verificar se o erro não interrompe o loop principal, mas a página é contada como processada.
  6.  **Normalização de URL (no contexto do crawling):**
      - Testar se a adição de URLs com fragmentos ou case diferente são tratadas corretamente pelo conjunto de visitadas/fila.
  7.  **Configuração do Crawler:**
      - Testar se os limites `max_pages` e `max_depth` passados via construtor ou `config` são respeitados.
      - O teste original usava um helper `_get_config_for_crawler` para simular um objeto `ConfigParser` a partir de um dicionário. Isso pode ser mantido ou adaptado.

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/core/test_crawler_integration.py`.
  - Utilizar `unittest` e `unittest.mock` extensivamente.
  - Usar `tempfile.mkdtemp()` para diretórios de saída temporários, se necessário para o mock do `writer`.

## Critérios de Aceitação
- Cenários de crawling de ponta a ponta são testados, incluindo limites e tratamento de erros.
- Mocks são usados corretamente para simular o comportamento das dependências.
- As interações entre o `Crawler` e seus componentes são validadas.
- Os testes passam consistentemente.
---
