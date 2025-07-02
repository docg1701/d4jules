---
id: task-D11
title: "Implementar extração de conteúdo e links com BeautifulSoup"
type: development
status: backlog
priority: medium
dependencies: ["task-R03"] # Conhecimento de BeautifulSoup
parent_plan_objective_id: "3.4.2"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "parser", "beautifulsoup", "core"]
description: |
  Desenvolver uma função ou método, preferencialmente em `d4jules/core/parser.py`, que utilize a biblioteca BeautifulSoup para processar o HTML de uma página.
  A função deve:
  1. Aceitar o conteúdo HTML de uma página e os seletores CSS (content_selector, navigation_selector, next_page_selector) como entrada.
  2. Parsear o HTML usando `BeautifulSoup` (com o parser `lxml` ou `html.parser`).
  3. Extrair o bloco de HTML correspondente ao `content_selector`. Se o seletor não encontrar nada, deve-se lidar com isso (ex: retornar None ou string vazia para o conteúdo).
  4. Encontrar todas as tags `<a>` dentro do elemento(s) correspondente ao `navigation_selector`. Para cada tag `<a>`, extrair o valor do atributo `href`.
  5. Se `next_page_selector` for fornecido e encontrado, extrair o `href` do link da próxima página.
  6. Normalizar todas as URLs extraídas para serem absolutas, utilizando a URL base da página original.
  7. Retornar o HTML do conteúdo principal e uma lista de novas URLs (links de navegação + link da próxima página, se houver).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "Implementação concluída e todos os testes unitários passaram."
# start_time: YYYY-MM-DDTHH:MM:SSZ # Placeholder, a ser preenchido pela plataforma
# end_time: YYYY-MM-DDTHH:MM:SSZ # Placeholder, a ser preenchido pela plataforma
# duration_minutes: 0 # Placeholder, a ser preenchido pela plataforma
# files_modified:
#   - d4jules/core/parser.py
#   - d4jules/tests/test_parser.py
#   - requirements.txt # Added lxml
# reference_documents_consulted:
#   - jules-flow/in_progress/task-D11.md # Task description
#   - jules-flow/docs/reference/beautifulsoup_research.md # BeautifulSoup usage
#   - https://docs.python.org/3/library/unittest.html # For test creation
#   - https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin # For URL normalization
# execution_details: |
#   1. Criado o arquivo `d4jules/core/parser.py`.
#   2. Implementada a função `parse_html_content(html_doc: str, base_url: str, content_selector: str, nav_selector: Optional[str], next_page_selector: Optional[str]) -> Tuple[Optional[str], List[str]]`.
#      - Utiliza `BeautifulSoup` com `lxml` (fallback para `html.parser`).
#      - Extrai o HTML do conteúdo principal usando `soup.select_one(content_selector)`.
#      - Extrai links de navegação de `a[href]` dentro do `nav_selector` (se fornecido).
#      - Extrai o link da próxima página de `a[href]` no/dentro do `next_page_selector` (se fornecido), com lógica refinada para tratar o seletor como link direto ou container.
#      - Normaliza todas as URLs para absolutas usando `urllib.parse.urljoin`.
#      - Retorna o HTML do conteúdo e uma lista ordenada e única de URLs.
#      - Lida com casos onde seletores não encontram elementos, retornando `None` para o conteúdo ou listas vazias de URLs.
#   3. Adicionado `lxml` ao `requirements.txt` e instalado dependências.
#   4. Criado o arquivo `d4jules/tests/test_parser.py` com 11 casos de teste abrangendo:
#      - Extração básica de conteúdo e links.
#      - Normalização de URLs (absolutas, relativas, diferentes bases).
#      - Casos de seletores não encontrados ou não fornecidos para conteúdo, navegação e próxima página.
#      - Tratamento de URLs duplicadas.
#   5. Executados os testes unitários, todos passaram.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/core/parser.py` (criação/modificação)

## Critérios de Aceitação
1.  A função parseia o HTML corretamente usando BeautifulSoup.
2.  O bloco de HTML do conteúdo principal é extraído com base no `content_selector`.
3.  URLs de links de navegação são extraídas com base no `navigation_selector`.
4.  URL do link da próxima página é extraída (se o seletor for fornecido e o link existir).
5.  Todas as URLs extraídas são convertidas para URLs absolutas.
6.  A função retorna o HTML do conteúdo e a lista de URLs normalizadas.
7.  A função lida corretamente com casos onde os seletores não encontram correspondências.

## Observações Adicionais
A biblioteca `urllib.parse.urljoin` pode ser útil para converter URLs relativas em absolutas.
```
