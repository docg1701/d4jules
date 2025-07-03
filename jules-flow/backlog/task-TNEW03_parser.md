---
id: task-TNEW03_parser
title: "Reescrever testes para src/core/parser.py"
type: test
status: backlog
priority: high
dependencies: ["task-D11"] # Depends on the parser implementation
parent_plan_objective_id: null
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "parser", "html", "beautifulsoup", "core"]
description: |
  Reescrever os testes unitários para o módulo `src/core/parser.py`.
  Os testes originais (`tests/core/test_parser.py`) foram apagados.

  **Funcionalidades a serem testadas (com base no `tests/core/test_parser.py` original e `task-D11`):**
  A função principal é `parse_html_content(html_doc, base_url, content_selector, nav_selector, next_page_selector)`.
  1.  **Extração Básica:**
      - Fornecer HTML de exemplo com conteúdo principal, links de navegação e link de próxima página.
      - Verificar se o HTML do conteúdo principal é extraído corretamente.
      - Verificar se todos os URLs (navegação, próxima página) são extraídos, normalizados para absolutos e retornados de forma única e ordenada.
  2.  **Casos de Seletores Não Encontrados:**
      - Testar quando `content_selector` não encontra nada (conteúdo HTML deve ser `None`).
      - Testar quando `nav_selector` não encontra nada ou não contém links `<a>`.
      - Testar quando `next_page_selector` não encontra nada.
  3.  **Seletores Ausentes (None):**
      - Testar comportamento quando `nav_selector` é `None`.
      - Testar comportamento quando `next_page_selector` é `None`.
  4.  **Resolução de URL:**
      - Testar com diferentes `base_url` (com e sem trailing slash) para garantir que links relativos, absolutos de caminho e absolutos completos sejam resolvidos corretamente.
      - Testar links como `link1.html`, `/abs/link2.html`, `../up/link3.html`, `http://other.com/link4.html`.
  5.  **Manipulação de Seletores de Próxima Página:**
      - Testar quando `next_page_selector` aponta diretamente para a tag `<a>`.
      - Testar quando `next_page_selector` aponta para um container que contém a tag `<a>`.
  6.  **Duplicação de URLs:**
      - Garantir que URLs duplicadas (mesmo que de fontes diferentes como navegação e próxima página, ou múltiplas ocorrências na navegação) sejam retornadas apenas uma vez.
  7.  **Fallback do Parser LXML:**
      - Embora difícil de testar diretamente sem controlar a disponibilidade do `lxml`, a lógica de fallback para `html.parser` deve ser considerada (o código original tem um try-except para isso).

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/core/test_parser.py`.
  - Utilizar `unittest`.
  - Pode ser útil usar `bs4.BeautifulSoup` dentro dos testes para normalizar o HTML esperado para comparação, como feito no teste original.

## Critérios de Aceitação
- Cobertura abrangente dos cenários de parsing de HTML.
- Os testes verificam a correta extração de conteúdo e a lista de URLs.
- A resolução de URLs relativas e absolutas é validada.
- Os testes passam consistentemente.
---
