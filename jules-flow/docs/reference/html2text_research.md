# Pesquisa sobre html2text

## Introdução
`html2text` é uma biblioteca Python que converte HTML para o formato Markdown.

## Instalação
```bash
pip install html2text
```
Ou clonando do repositório Git:
```bash
git clone --depth 50 https://github.com/Alir3z4/html2text.git
cd html2text
python -m build -nwx
python -m pip install --upgrade ./dist/*.whl
```

## Uso Básico
```python
import html2text

html_content = "<h1>Título</h1><p>Este é um <b>exemplo</b>.</p>"
markdown_output = html2text.html2text(html_content)
print(markdown_output)
# Saída:
# # Título
#
# Este é um **exemplo**.
```

## Uso com Opções de Configuração
É possível customizar a conversão instanciando `HTML2Text` e configurando suas propriedades.

```python
import html2text

h = html2text.HTML2Text()

# Exemplo de configuração de opções:
h.ignore_links = False # Padrão é False
h.body_width = 0       # 0 para não quebrar linhas (padrão é 78)
h.skip_internal_links = True # Padrão é True
h.inline_links = True  # Padrão é True. Se False, usa links de referência.
h.protect_links = False # Padrão é False
h.bypass_tables = False # Padrão é False. Se True, tabelas HTML são mantidas.
# ... outras opções

html_content = "<p>Visite <a href='http://example.com'>este site</a>.</p>"
markdown_output = h.handle(html_content)
print(markdown_output)
# Saída (com inline_links=True):
# Visite [este site](http://example.com).
#
# Saída (com inline_links=False):
# Visite [este site][1].
#
#  [1]: http://example.com
```

## Principais Opções de Configuração (via objeto `HTML2Text`)

Muitas opções podem ser ajustadas. As mais relevantes para o projeto `d4jules` (preservar estrutura e conteúdo) podem incluir:

*   **`body_width`**: (Inteiro) Largura da linha para quebra. `0` desabilita a quebra automática. (Padrão: `78`)
*   **`ignore_links`**: (Booleano) Se `True`, não formata links. (Padrão: `False`)
*   **`protect_links`**: (Booleano) Se `True`, protege links de quebras de linha envolvendo-os com `<` e `>`. (Padrão: `False`)
*   **`skip_internal_links`**: (Booleano) Se `True`, ignora links internos (ex: `#ancora`). (Padrão: `True`)
*   **`inline_links`**: (Booleano) Se `True`, usa links no formato `[texto](url)`. Se `False`, usa links de referência no final do documento. (Padrão: `True`)
*   **`ignore_images`**: (Booleano) Se `True`, não formata imagens. (Padrão: `False`)
*   **`images_as_html`**: (Booleano) Se `True`, sempre escreve tags `<img>` como HTML bruto, preservando `height`, `width`, `alt`. (Padrão: `False`)
*   **`images_to_alt`**: (Booleano) Se `True`, descarta dados da imagem, mantendo apenas o texto `alt`. (Padrão: `False`)
*   **`bypass_tables`**: (Booleano) Se `True`, formata tabelas em HTML em vez de Markdown. Pode ser útil para tabelas complexas que não têm boa representação em Markdown. (Padrão: `False`)
*   **`ignore_tables`**: (Booleano) Se `True`, ignora tags de tabela (`table`, `th`, `td`, `tr`) mas mantém o conteúdo das células em novas linhas. (Padrão: `False`)
*   **`single_line_break`**: (Booleano) Se `True`, usa uma única quebra de linha após um elemento de bloco em vez de duas. (Padrão: `False`)
*   **`wrap_links`**: (Booleano) Define se links devem ser quebrados durante a quebra de texto (implica `inline_links = False`). (Padrão: `True`)
*   **`wrap_list_items`**: (Booleano) Define se itens de lista devem ser quebrados durante a quebra de texto. (Padrão: `True`)
*   **`decode_errors`**: (String) Como lidar com erros de decodificação. Valores aceitáveis: `'strict'`, `'ignore'`, `'replace'`. (Padrão: `'strict'`)
*   **`default_image_alt`**: (String) Texto alternativo padrão para imagens sem atributo `alt`. (Padrão: `''`)
*   **`emphasis_mark`**: (String) Caractere para ênfase (`<em>`). Padrão: `'_'`. Pode ser alterado para `'*'`.
*   **`strong_mark`**: (String) Caractere para importância (`<strong>`). Padrão: `'**'`.

Para o `d4jules`, as seguintes configurações podem ser um bom ponto de partida para preservar ao máximo a estrutura e o conteúdo:
```python
h = html2text.HTML2Text()
h.body_width = 0  # Sem quebra de linha automática
h.single_line_break = False # Manter parágrafos separados
h.inline_links = True # Links inline são geralmente preferíveis para leitura
h.protect_links = True # Tentar proteger links longos
h.images_as_html = True # Preservar dimensões e alt de imagens
h.bypass_tables = False # Tentar converter tabelas para Markdown, se possível
h.ignore_emphasis = False # Manter ênfase
h.skip_internal_links = False # Manter links internos, podem ser úteis
# Considerar outras opções como wrap_list_items, wrap_tables se a quebra de linha for reativada.
```

## Interface de Linha de Comando (CLI)
`html2text` também pode ser usado via linha de comando.
Exemplo: `html2text file.html > file.md`

Algumas opções da CLI:
*   `--ignore-links`
*   `--protect-links`
*   `--ignore-images`
*   `--images-as-html`
*   `--body-width=0` (para desabilitar quebra de linha)
*   `--bypass-tables`
*   `--single-line-break`
*   `--no-automatic-links`
*   `--reference-links` (oposto de `inline_links`)

A lista completa de opções da CLI e programáticas está na documentação.

Referência principal: [GitHub - Alir3z4/html2text](https://github.com/Alir3z4/html2text) (especialmente o `README.md` e `docs/usage.md` se acessível).
A documentação fornecida pelo usuário foi a principal fonte para este resumo.
```
