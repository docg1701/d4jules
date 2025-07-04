---
id: task-R01
title: "Refatorar Crawler para Integrar Lógica de Scraping Completa"
type: refactor
status: backlog # Este status é do arquivo original, o status real está no task-index.md
priority: high
dependencies: []
parent_plan_objective_id: "Fase6-Review"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder, será atualizado
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder, será atualizado
tags: ["crawler", "core-logic", "scraping"]
description: |
  Refatorar o `Crawler` para integrar a lógica de análise de página (analyzer), parsing (parser) e escrita (writer) dentro do seu loop de processamento (`start_crawling` ou método similar).
  Atualmente, `Crawler.start_crawling` apenas gerencia a fila de URLs e imprime mensagens, mas não processa as páginas.
  O `scraper_cli.py` deverá ser ajustado para instanciar e injetar os componentes `Analyzer`, `Parser`, `Writer` (ou suas respectivas funções) no `Crawler`.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: ""
# start_time: 2024-07-04T10:00:00Z # Estimativa
# end_time: 2024-07-04T10:30:00Z # Estimativa
# duration_minutes: 30 # Estimativa
# files_modified:
#   - src/core/crawler.py
#   - src/scraper_cli.py
#   - tests/core/test_crawler.py
# reference_documents_consulted:
#   - VISION.md
# execution_details: |
#   1. Modificado `src/core/crawler.py`:
#      - Construtor (`__init__`) atualizado para aceitar funções de análise, parsing e escrita, além da configuração do analisador e diretório de saída, via injeção de dependência. Removido o parâmetro `config` genérico.
#      - Método `start_crawling` refatorado para orquestrar o processo completo de scraping para cada URL:
#        - Chama a função `analyzer_func` injetada para obter seletores CSS.
#        - Realiza um novo download do HTML da URL (TODO para otimização futura para evitar re-download).
#        - Chama a função `parser_func` injetada para extrair conteúdo e links.
#        - Chama a função `writer_func` injetada para salvar o conteúdo em Markdown.
#        - Adiciona novos links válidos à fila.
#        - Incluído tratamento básico de erro (print de mensagens) para cada etapa (análise, download, parse, escrita), permitindo que o crawler continue com a próxima URL em caso de falha em uma.
#   2. Modificado `src/scraper_cli.py`:
#      - Atualizada a instanciação do `Crawler` para passar as funções `analyze_url_for_selectors`, `parse_html_content`, `save_content_as_markdown` e as configurações necessárias (`analyzer_config_dict`, `output_dir`).
#      - Importadas as funções e exceções necessárias dos módulos do núcleo.
#   3. Modificado `tests/core/test_crawler.py`:
#      - `setUp` atualizado para mockar as novas dependências injetadas (`analyzer_func`, `parser_func`, `writer_func`, `analyzer_config`).
#      - Testes de inicialização ajustados.
#      - Adicionados novos testes para `start_crawling` cobrindo:
#        - Execução bem-sucedida de uma página.
#        - Falha na fase de análise (analyzer).
#        - Falha no download de HTML para o parser.
#        - Falha na fase de parsing.
#        - Falha na fase de escrita.
#        - Verificação do limite `max_pages`.
#      - Os testes verificam se as funções mockadas são chamadas com os argumentos corretos e se o estado do crawler (fila, visitados) é atualizado como esperado.
#
# A funcionalidade crítica de scraping agora está integrada ao Crawler.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/crawler.py`
* `src/scraper_cli.py`
* `src/core/analyzer.py`
* `src/core/parser.py`
* `src/core/writer.py`

## Critérios de Aceitação
1. O método `Crawler.start_crawling()` (ou um novo método chamado por ele) orquestra o ciclo completo:
    a. Obter URL da fila.
    b. Chamar o `analyzer` para obter seletores.
    c. Chamar o `parser` para extrair conteúdo HTML e novos links.
    d. Chamar o `writer` para salvar o conteúdo em Markdown.
    e. Adicionar novos links válidos à fila do `Crawler`.
2. O `scraper_cli.py` instancia os componentes `Analyzer`, `Parser`, `Writer` (ou as funções relevantes) e os passa para o `Crawler` durante sua inicialização.
3. A funcionalidade de scraping completa (download, análise, parse, escrita) está operacional.
4. Os testes existentes para `crawler`, `analyzer`, `parser`, `writer` ainda passam (ou são ajustados conforme necessário se a interface mudar).
5. (Ideal) Novos testes de integração são criados para verificar o fluxo completo através do `Crawler` para uma ou duas páginas mockadas.

## Observações Adicionais
Esta é uma refatoração crítica para tornar a aplicação funcional. Considerar como lidar com os objetos de configuração e a chave de API, que precisam ser acessíveis ao `analyzer`.
O `Crawler` pode precisar de acesso ao objeto de configuração completo ou a partes dele.
A injeção de dependência (passar instâncias de analyzer, parser, writer para o Crawler) é a abordagem preferida.
