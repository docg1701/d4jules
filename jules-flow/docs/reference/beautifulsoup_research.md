# Pesquisa sobre Beautiful Soup

## Instalação
```bash
pip install beautifulsoup4
# Também é recomendado instalar um parser eficiente, como o lxml:
pip install lxml
# Ou html5lib para parsear como um navegador:
# pip install html5lib
```

## Parsing de HTML
Para parsear um documento HTML, passe o conteúdo HTML (string ou filehandle) e o nome do parser para o construtor `BeautifulSoup`.
```python
from bs4 import BeautifulSoup

html_string = "<html><head><title>Título da Página</title></head><body><p class='info'>Conteúdo aqui.</p><a>Link</a></body></html>"

# Usando lxml (rápido, recomendado)
soup = BeautifulSoup(html_string, 'lxml')

# Usando o parser padrão do Python
# soup = BeautifulSoup(html_string, 'html.parser')

# Usando html5lib (parseia como um navegador, mais lento mas robusto para HTML malformado)
# soup = BeautifulSoup(html_string, 'html5lib')
```

## Extração de Conteúdo com Seletores

Beautiful Soup permite navegar e pesquisar na árvore de parse de várias formas.

### Usando Nomes de Tags
Acesso direto à primeira tag com um nome específico:
```python
print(soup.title)  # <title>Título da Página</title>
print(soup.title.string)  # Título da Página
print(soup.p)  # <p class="info">Conteúdo aqui.</p>
```

### `find()` e `find_all()`
*   `find(name, attrs, string, **kwargs)`: Retorna a primeira tag ou string que corresponde aos filtros.
*   `find_all(name, attrs, recursive, string, limit, **kwargs)`: Retorna uma lista de todas as tags ou strings que correspondem aos filtros.

**Filtrando por nome da tag:**
```python
all_a_tags = soup.find_all('a') # Retorna uma lista de todas as tags <a>
first_a_tag = soup.find('a')
```

**Filtrando por atributos:**
```python
# Por classe CSS (usar 'class_' porque 'class' é palavra reservada em Python)
info_paragraphs = soup.find_all('p', class_='info')

# Por ID
element_with_id = soup.find(id='meu_id')

# Por qualquer atributo
links_com_href = soup.find_all(href=True) # Encontra todas as tags que possuem o atributo href
link_especifico = soup.find('a', href='http://example.com')
```

**Filtrando por string (conteúdo textual):**
```python
import re
text_element = soup.find(string='Conteúdo aqui.')
elements_com_padrao = soup.find_all(string=re.compile("Título"))
```

### Seletores CSS
Beautiful Soup suporta seletores CSS através do método `.select()` (que retorna uma lista) e `.select_one()` (que retorna o primeiro elemento). Requer a biblioteca `soupsieve` (geralmente instalada com `beautifulsoup4`).

```python
# Selecionar por nome da tag
titles = soup.select('title') # [<title>Título da Página</title>]

# Selecionar por classe CSS
info_elements = soup.select('.info') # [<p class="info">Conteúdo aqui.</p>]

# Selecionar por ID
el_by_id = soup.select_one('#meu_id')

# Seletores mais complexos
# Tag 'a' dentro de um elemento com classe 'menu'
menu_links = soup.select('.menu a')

# Selecionar elementos <p> que são filhos diretos de <body>
direct_p_children = soup.select('body > p')

# Selecionar por atributo
links_example = soup.select('a[href="http://example.com"]')
```
Referência: [CSS Selectors](https://beautiful-soup-4.readthedocs.io/en/latest/#css-selectors)

## Extração de URLs de Links
Após selecionar uma tag `<a>`, o atributo `href` pode ser acessado como um dicionário:
```python
all_links = soup.find_all('a')
for link_tag in all_links:
    url = link_tag.get('href') # Usar .get() é mais seguro caso o atributo não exista
    if url:
        print(url)
```

## Obter HTML/Texto Limpo

**Obter o texto de uma tag e seus descendentes:**
`.get_text()` retorna todo o texto dentro de uma tag, concatenado.
```python
paragrafo_tag = soup.find('p', class_='info')
if paragrafo_tag:
    texto_do_paragrafo = paragrafo_tag.get_text()
    print(texto_do_paragrafo) # "Conteúdo aqui."

    # Para remover espaços em branco extras nas bordas e juntar com um separador:
    texto_limpo = paragrafo_tag.get_text(separator=' ', strip=True)
    print(texto_limpo)
```

**Obter o HTML interno de uma tag:**
Converter a tag para string ou usar `.decode_contents()`.
```python
div_content = soup.find('div', id='main_content')
if div_content:
    inner_html = div_content.decode_contents() # HTML interno como string
    # ou para obter a tag e seu conteúdo:
    # outer_html = str(div_content)
    # print(inner_html)
```

**Obter o conteúdo completo de um seletor (incluindo tags filhas):**
Se o seletor CSS (`content_selector` obtido do LLM) aponta para um elemento que contém o conteúdo principal, você pode primeiro encontrar esse elemento e depois extrair seu HTML ou texto.

```python
# Supondo que content_selector = "article.main-content-area"
main_content_element = soup.select_one("article.main-content-area")
if main_content_element:
    # Para obter todo o HTML dessa seção:
    html_da_secao = str(main_content_element)

    # Para obter todo o texto dessa seção:
    texto_da_secao = main_content_element.get_text(separator='\\n', strip=True)
    # print(texto_da_secao)
```

## Navegação na Árvore
Beautiful Soup permite navegar pela árvore de elementos:
*   `.parent`, `.parents`
*   `.contents`, `.children`, `.descendants`
*   `.next_sibling`, `.previous_sibling`, `.next_siblings`, `.previous_siblings`

Referência principal: [Beautiful Soup Documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)
```
