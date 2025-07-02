---
id: task-D12
title: "Implementar conversão para Markdown e salvamento de arquivos"
type: development
status: backlog
priority: medium
dependencies: ["task-R04", "task-D01"] # R04 para conhecimento html2text, D01 para d4jules/output/
parent_plan_objective_id: "3.4.3"
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
tags: ["development", "python", "markdown", "html2text", "fileio", "core"]
description: |
  Desenvolver uma função ou método, preferencialmente em `d4jules/core/writer.py`, para converter o conteúdo HTML (extraído na task D11) para o formato Markdown e salvá-lo em um arquivo.
  A função deve:
  1. Aceitar o HTML do conteúdo principal de uma página e a URL original da página (para nomear o arquivo) como entrada.
  2. Utilizar a biblioteca `html2text` para converter o HTML para Markdown. Configurar `html2text` com opções que preservem a estrutura e o conteúdo da melhor forma possível (ver `html2text_research.md`).
  3. Gerar um nome de arquivo para o Markdown. O nome deve ser derivado da URL original, tornando-o único e informativo (ex: limpar caracteres especiais da URL, usar partes do caminho, e adicionar `.md`).
  4. Salvar o conteúdo Markdown no diretório `d4jules/output/`. Certificar-se de que o diretório de saída exista (pode ser criado na task D01 ou verificado aqui).

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
#   - d4jules/core/writer.py
# reference_documents_consulted:
#   - jules-flow/working-plan.md
#   - jules-flow/docs/reference/html2text_research.md
# execution_details: |
#   Criado `d4jules/core/writer.py`.
#   Implementada função `save_markdown(url, html_content)` que:
#     - Instancia `html2text.HTML2Text()` e configura opções (ex: `body_width=0`, `images_as_html=True`).
#     - Converte `html_content` para Markdown usando `h.handle(html_content)`.
#     - Gera nome de arquivo a partir da URL (limpando-a, ex: `example_com_path_to_page.md`).
#     - Cria o diretório `d4jules/output/` se não existir (usando `os.makedirs(exist_ok=True)`).
#     - Salva o Markdown no arquivo dentro de `d4jules/output/`.
#   Adicionado tratamento básico de erros para escrita de arquivo.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `d4jules/core/writer.py` (criação/modificação)
* `d4jules/output/` (diretório de escrita)

## Critérios de Aceitação
1.  A função converte corretamente o HTML fornecido para Markdown usando `html2text`.
2.  As opções do `html2text` são configuradas para otimizar a preservação da estrutura do conteúdo.
3.  Um nome de arquivo apropriado e seguro é gerado a partir da URL.
4.  O arquivo Markdown é salvo no diretório `d4jules/output/`.
5.  A função lida com possíveis erros durante a conversão ou escrita do arquivo.

## Observações Adicionais
A lógica de nomeação de arquivos deve evitar conflitos e caracteres inválidos em nomes de arquivo. Pode-se usar `pathlib` para manipulação de caminhos.
```
