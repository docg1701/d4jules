# Pesquisa sobre Google Gemini API (Python SDK)

## Configuração e Autenticação

**Instalação do SDK:**
```bash
pip install -q -U google-generativeai
```

**Configuração da API Key:**
A API key deve ser configurada, preferencialmente como uma variável de ambiente `GOOGLE_API_KEY`.
```python
import google.generativeai as genai
import os

# os.environ["GOOGLE_API_KEY"] = "SUA_API_KEY_AQUI" # Não recomendado em código
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```
Alternativamente, pode ser passada diretamente ao instanciar o cliente, mas o uso de variáveis de ambiente é mais seguro.

Referência: [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/get-started/python)

## Envio de Requisições e Configuração do Modelo

**Modelos Disponíveis:**
Gemini oferece vários modelos, como `gemini-1.5-flash-latest`, `gemini-1.5-pro-latest`, etc. `gemini-1.5-flash` é uma boa opção para tarefas que exigem baixa latência e custo.

**Geração de Conteúdo (Texto):**
```python
model = genai.GenerativeModel('gemini-1.5-flash-latest')

prompt = "Explique o conceito de Machine Learning para um leigo."
response = model.generate_content(prompt)
print(response.text)
```

**Configurações de Geração:**
É possível configurar parâmetros como `temperature`, `max_output_tokens`, `stop_sequences`, etc., através do argumento `generation_config`.
```python
response = model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=2048
    )
)
```

## Análise de HTML e Saída Estruturada (JSON)

A Gemini API suporta a geração de saídas estruturadas, o que é essencial para extrair seletores de HTML. A forma recomendada é configurar um `response_schema` no modelo.

**Definindo um Schema com Pydantic (preferencial no Python SDK):**
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class HtmlSelectors(BaseModel):
    """Define os seletores CSS para extrair informações de uma página HTML."""
    content_selector: str = Field(description="Seletor CSS para o bloco de conteúdo principal da página.")
    navigation_links_selector: str = Field(description="Seletor CSS que aponta para os links de navegação internos do site (ex: menu, outros artigos).")
    next_page_button_selector: Optional[str] = Field(default=None, description="Seletor CSS para o botão/link 'Próxima Página', se houver.")

# Configurando o modelo para usar o schema
model_for_json = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    generation_config=genai.types.GenerationConfig(
        response_mime_type="application/json",
        response_schema=HtmlSelectors # Pode ser uma classe Pydantic ou uma lista dela
    )
)

# Exemplo de prompt para análise de HTML
html_content = """
<!DOCTYPE html>
<html>
<head><title>Exemplo</title></head>
<body>
  <article class='content-main'><h1>Título</h1><p>Parágrafo 1...</p></article>
  <nav class='menu-nav'><a href='/page1'>P1</a><a href='/page2'>P2</a></nav>
  <a href='?page=2' class='next-btn'>Próxima</a>
</body>
</html>
""" # Conteúdo HTML simplificado

prompt_analise_html = f"""
Analise o seguinte código HTML e identifique os seletores CSS para:
1. A área principal de conteúdo.
2. Os links de navegação principais do site.
3. O botão ou link para a "próxima página", se existir.

Considere a semântica e estrutura comum de páginas web.

HTML:
```html
{html_content}
```
Responda estritamente no formato JSON especificado.
"""

response_json = model_for_json.generate_content(prompt_analise_html)

# A resposta em response_json.text será uma string JSON.
# O SDK também tenta parsear para o objeto Pydantic em response_json.candidates[0].content.parts[0].function_call (se usando function calling implícito)
# ou diretamente via response.parsed se o SDK evoluir para tal (verificar documentação mais recente para parsing direto).

# Para acessar o JSON diretamente (mais robusto inicialmente):
import json
try:
    # A API Gemini, quando configurada com response_mime_type="application/json",
    # deve retornar o JSON diretamente no campo 'text'.
    parsed_selectors = json.loads(response_json.text)
    print(parsed_selectors)
    # Se o schema for uma classe Pydantic, pode-se instanciar:
    # selectors_obj = HtmlSelectors(**parsed_selectors)
    # print(selectors_obj.content_selector)
except json.JSONDecodeError:
    print("Erro ao decodificar JSON:", response_json.text)
except AttributeError: # Caso .text não seja o caminho direto para o JSON
    # Tentar inspecionar response_json.parts ou response_json.candidates
    # para encontrar a string JSON. A estrutura exata da resposta pode variar
    # ligeiramente com atualizações do SDK ou se a interpretação do schema
    # levar a um "function call" implícito.
    # No caso de `langchain-google-genai`, ele abstrai isso e retorna o objeto parseado.
    # Com `google-generativeai` puro, o `response.text` é o mais comum para JSON direto.
    print("Não foi possível acessar .text, inspecione o objeto de resposta:", response_json)


```

**Considerações:**
*   **`response_mime_type="application/json"`**: Crucial para instruir o modelo a gerar JSON.
*   **`response_schema`**: Fornece a estrutura esperada. Pode ser uma classe Pydantic, uma `typing.TypedDict`, ou um dicionário representando o JSON Schema. Pydantic é conveniente no Python.
*   **Prompting**: O prompt deve ser claro sobre a tarefa (analisar HTML, extrair seletores CSS) e pode incluir exemplos (few-shot) para casos complexos.
*   **Tratamento da Resposta**: A resposta virá como uma string JSON no atributo `.text` do objeto de resposta quando `response_mime_type` é `application/json`. É necessário parsear essa string JSON. Algumas versões ou configurações do SDK podem oferecer o objeto já parseado (ex: `response.parsed` ou via `response.candidates[0].content.parts[0].function_call.args` se o modelo usar function calling internamente para aderir ao schema). Recomenda-se verificar a documentação da versão específica do SDK para a forma mais direta de acessar o JSON parseado.

Referência: [Structured Output with Gemini API](https://ai.google.dev/gemini-api/docs/structured-output)

## Limitações e Boas Práticas
*   **Tamanho do Prompt/Schema**: O schema conta para o limite de tokens de entrada. Schemas complexos podem levar a erros.
*   **Qualidade da Saída**: Se os resultados não forem os esperados, refine o prompt ou simplifique o schema.
*   **Obrigatoriedade de Campos**: Por padrão, campos no schema são opcionais. Use `required` no JSON Schema ou defina campos sem `Optional` em Pydantic para torná-los obrigatórios.

URL de referência principal do SDK: `https://github.com/google/generative-ai-python`
Documentação principal: `https://ai.google.dev/gemini-api/docs`
```
