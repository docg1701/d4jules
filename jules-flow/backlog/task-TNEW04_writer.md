---
id: task-TNEW04_writer
title: "Reescrever testes para src/core/writer.py"
type: test
status: backlog
priority: high
dependencies: ["task-D12"] # Depends on the writer implementation
parent_plan_objective_id: null
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for current time
tags: ["test", "python", "writer", "markdown", "fileio", "core"]
description: |
  Reescrever os testes unitários para o módulo `src/core/writer.py`.
  Os testes originais (`tests/core/test_writer.py`) foram apagados.

  **Funcionalidades a serem testadas (com base no `tests/core/test_writer.py` original e `task-D12`):**

  **1. `_generate_filename_from_url(page_url: str) -> str`:**
      - URLs simples (http, https, com/sem trailing slash).
      - URLs com caminhos.
      - URLs com caminhos terminando em `.html` ou outras extensões.
      - URLs com query parameters e fragmentos (devem ser ignorados para o nome do arquivo).
      - URLs com caracteres especiais no caminho (devem ser limpos/substituídos).
      - URLs que já terminam com `.md` no caminho.
      - URLs resultando em nomes de arquivo vazios ou apenas com separadores (deve usar "index.md").
      - URLs longas que exigem truncamento (verificar `MAX_FILENAME_LENGTH`).
      - URLs com `localhost` e porta.

  **2. `save_content_as_markdown(page_url: str, html_content: Optional[str], output_dir: str) -> Optional[str]`:**
      - Salvar conteúdo HTML básico e verificar se o arquivo Markdown é criado com o nome esperado.
      - Verificar se o conteúdo do arquivo Markdown corresponde (aproximadamente) ao HTML convertido (considerar variações do `html2text`).
      - Testar com `html_content = None` (nenhum arquivo deve ser criado, deve retornar `None`).
      - Testar a criação do `output_dir` (incluindo diretórios aninhados) se não existir.
      - Integrar com a geração de nome de arquivo para garantir que nomes complexos sejam tratados corretamente.
      - (Opcional, se implementado no `writer.py`) Testar tratamento de erros de conversão do `html2text`.
      - (Opcional, se implementado no `writer.py`) Testar tratamento de erros de I/O durante a escrita do arquivo.

  **Estrutura do Arquivo de Teste:**
  - O novo arquivo de teste deve ser criado em `tests/core/test_writer.py`.
  - Utilizar `unittest`.
  - Usar `tempfile.mkdtemp()` para criar diretórios de saída temporários e `shutil.rmtree()` para limpeza em `setUp` e `tearDown`.
  - Usar `pathlib.Path` para manipulação de caminhos.

## Critérios de Aceitação
- Cobertura completa da lógica de geração de nomes de arquivo.
- Validação da funcionalidade de salvamento de Markdown, incluindo criação de diretório.
- Os testes devem limpar os arquivos/diretórios temporários criados.
- Os testes passam consistentemente.
---
