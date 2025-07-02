---
id: task-D13
title: "Implementar lógica principal de orquestração do crawling"
type: development
status: backlog
priority: high
dependencies: ["task-D09", "task-D10", "task-D11", "task-D12"]
parent_plan_objective_id: "3.4.4"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "crawler", "core", "orchestration"]
description: |
  Desenvolver a lógica central de orquestração do processo de crawling, preferencialmente na classe `Crawler` em `d4jules/core/crawler.py` ou como função principal em `d4jules/scraper_cli.py`.
  Esta lógica deve:
  1. Inicializar com a URL base fornecida pelo usuário. Adicionar esta URL à fila de URLs a visitar (gerenciada pela task D10).
  2. Entrar em um loop que continua enquanto a fila de URLs não estiver vazia (ou um limite de páginas/profundidade for atingido, se implementado).
  3. Em cada iteração:
      a. Obter a próxima URL da fila (D10).
      b. Se a URL já foi visitada, pular para a próxima.
      c. Marcar a URL atual como visitada (D10).
      d. Chamar a função de análise de LLM (D09) para obter os seletores CSS para a URL atual.
      e. Se os seletores forem obtidos com sucesso:
          i. Baixar o HTML da URL atual (pode ser reutilizado do D09 ou feito novamente).
          ii. Chamar a função de parsing (D11) com o HTML e os seletores para extrair o conteúdo principal e novos links.
          iii. Chamar a função de escrita (D12) para converter o conteúdo principal para Markdown e salvá-lo.
          iv. Adicionar os novos links (normalizados para URLs absolutas e filtrados para pertencerem ao mesmo domínio/subdomínio da URL base) à fila de URLs a visitar (D10).
  4. Lidar com erros em cada etapa (ex: falha no download, falha na análise LLM, falha no parsing) de forma que o crawler possa continuar com outras URLs se possível (ex: logar o erro e prosseguir).
  5. Opcional: Implementar um limite para o número de páginas a serem rastreadas ou profundidade máxima para evitar crawling excessivo.

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
#   - d4jules/core/crawler.py
#   - d4jules/scraper_cli.py (para iniciar o crawler)
# reference_documents_consulted:
#   - jules-flow/working-plan.md
#   - task-D09.md
#   - task-D10.md
#   - task-D11.md
#   - task-D12.md
# execution_details: |
#   Implementada a classe `Crawler` em `d4jules/core/crawler.py` com um método `start_crawling(base_url)`.
#   O método `start_crawling` orquestra o loop:
#     - Usa `analyzer.analyze_url_for_selectors()`.
#     - Usa `requests` para baixar HTML (reutilizando ou baixando novamente).
#     - Usa `parser.parse_html_content()`.
#     - Usa `writer.save_markdown()`.
#     - Usa os métodos da própria classe Crawler para gerenciar fila e visitados.
#   Adicionado filtro para que apenas URLs do mesmo domínio da URL base sejam adicionadas à fila.
#   Tratamento básico de exceções para cada etapa do processamento de uma URL.
#   O `scraper_cli.py` é atualizado para instanciar e chamar `crawler.start_crawling()`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/core/crawler.py` (criação/modificação)
* `d4jules/scraper_cli.py` (para iniciar o processo de crawling)
* `d4jules/core/analyzer.py` (utilização)
* `d4jules/core/parser.py` (utilização)
* `d4jules/core/writer.py` (utilização)

## Critérios de Aceitação
1.  O crawler inicia com a URL base e a processa.
2.  O crawler itera sobre as URLs encontradas, respeitando o controle de visitas.
3.  Para cada URL válida, o conteúdo é analisado, parseado, convertido para Markdown e salvo.
4.  Novos links (do mesmo domínio) são adicionados à fila para processamento futuro.
5.  O processo lida com erros de forma robusta, permitindo que o crawling continue se possível.
6.  O crawling para quando a fila está vazia (ou um limite opcional é atingido).

## Observações Adicionais
A filtragem de URLs para o mesmo domínio é importante para evitar que o crawler saia do site alvo. Pode-se usar `urllib.parse.urlparse` para verificar o `netloc`.
```
