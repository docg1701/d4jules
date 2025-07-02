---
id: task-T02
title: "Testar funcionalidade completa do scraper_cli.py"
type: test
status: backlog
priority: high
dependencies: ["task-D01", "task-D07", "task-D08", "task-D13"] # Depende da estrutura, config, input e orquestração do crawler
parent_plan_objective_id: "Passo3-Test" # Referência ao teste do Passo 3 do working-plan
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["test", "integration", "cli", "python", "e2e"]
description: |
  Realizar um teste de integração ponta a ponta (end-to-end) do script `d4jules/scraper_cli.py`.
  Este teste deve verificar o fluxo completo da aplicação:
  1.  O script `scraper_cli.py` é executado (preferencialmente via `start.sh` para incluir o setup do ambiente).
  2.  Carregamento das configurações do `d4jules/config.ini` (API key e modelo LLM).
  3.  Solicitação da URL ao usuário. Fornecer uma URL de um site de documentação pequeno e simples para o teste.
  4.  Análise da URL inicial pelo LLM para obter seletores (para este teste, a chamada real ao LLM pode ser mockada para retornar seletores predefinidos e válidos para a URL de teste, a fim de tornar o teste mais rápido, controlável e não dependente de cotas de API. O teste de D09 já cobre a interação real com o LLM).
  5.  Início do processo de crawling com base na URL e seletores (mockados ou reais).
  6.  O crawler deve visitar algumas páginas (a URL inicial e alguns links internos encontrados).
  7.  Para cada página visitada:
      a.  Extração do conteúdo principal usando BeautifulSoup e o `content_selector`.
      b.  Conversão do conteúdo para Markdown usando `html2text`.
      c.  Salvamento do arquivo Markdown no diretório `d4jules/output/`. O nome do arquivo deve ser previsível.
  8.  Verificar se os arquivos Markdown esperados são criados em `d4jules/output/` e se o conteúdo parece razoável (sem verificar a exatidão byte a byte do Markdown, mas sim a presença de texto).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified: [] # Apenas verifica arquivos em d4jules/output/
# reference_documents_consulted:
#   - jules-flow/working-plan.md
#   - Todas as tasks de desenvolvimento D01 a D13.
# execution_details: |
#   - Configurar `d4jules/config.ini` com uma API key válida (ou preparar mock para LLM).
#   - Escolher uma URL de teste simples (ex: uma página estática com alguns links internos).
#   - (Opcional, recomendado) Modificar `d4jules/core/analyzer.py` temporariamente para retornar seletores mockados para a URL de teste.
#   - Executar `bash start.sh`.
#   - Fornecer a URL de teste quando solicitado.
#   - Após a execução, verificar o conteúdo do diretório `d4jules/output/`.
#   - Confirmar que os arquivos .md esperados foram criados e contêm texto.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `start.sh` (para execução)
* `d4jules/scraper_cli.py` (o script principal sendo testado)
* `d4jules/config.ini` (para configuração)
* Conteúdo do diretório `d4jules/output/` (para verificação dos resultados)
* Uma URL de um site de documentação real, porém simples, para teste.

## Critérios de Aceitação
1.  A aplicação é iniciada via `start.sh` (ou `python d4jules/scraper_cli.py` diretamente após setup manual do venv).
2.  As configurações são carregadas e a URL é solicitada.
3.  O processo de crawling é iniciado e processa algumas páginas.
4.  Arquivos Markdown correspondentes às páginas rastreadas são criados no diretório `d4jules/output/`.
5.  Os arquivos Markdown contêm o conteúdo textual esperado das páginas.
6.  A aplicação finaliza sem erros inesperados (erros de rede ou do site alvo podem ocorrer, mas a aplicação deve lidar com eles de forma minimamente graciosa).

## Observações Adicionais
Este é um teste de integração crucial. Se a chamada ao LLM for mockada, deve-se garantir que os seletores mockados sejam válidos para a URL de teste. O foco é no fluxo de crawling, parsing e escrita.
```
