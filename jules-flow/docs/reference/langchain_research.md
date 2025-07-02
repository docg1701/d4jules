# Pesquisa sobre LangChain (Python)

## Integração com Google Gemini

A integração do LangChain com os modelos Google Gemini é feita através do pacote `langchain-google-genai`.

**Instalação:**
```bash
pip install langchain-google-genai
```

**Uso Básico (Chat Model):**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Configurar a API Key (idealmente via variável de ambiente)
# os.environ["GOOGLE_API_KEY"] = "SUA_API_KEY"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") # ou gemini-1.5-pro, etc.

# Exemplo de invocação
messages = [
    ("system", "Você é um assistente prestativo."),
    ("human", "Qual o significado da vida?"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
```

Referência: [LangChain Google Generative AI Docs](https://python.langchain.com/v0.2/docs/integrations/chat/google_generative_ai/)

## Gerenciamento de Prompts

LangChain facilita o gerenciamento de prompts através de `ChatPromptTemplate`.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor de {input_language} para {output_language}."),
    ("human", "{input_text}"),
])

chain = prompt | llm # LLM definido como no exemplo anterior

response = chain.invoke({
    "input_language": "inglês",
    "output_language": "francês",
    "input_text": "Hello, world!"
})
print(response.content)
```

## Processamento de Respostas do LLM (Saída Estruturada / JSON)

Para obter saídas estruturadas (como JSON) de modelos que suportam "tool calling" ou "JSON mode", LangChain oferece o método `.with_structured_output()`. Isso é crucial para extrair seletores de conteúdo e navegação.

**Modelos Suportados:** Verificar a lista de modelos que suportam este método na documentação do LangChain. Gemini está entre eles.

**Usando com Pydantic Models:**
```python
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional

class SiteStructure(BaseModel):
    """Estrutura de um site para scraping."""
    content_selector: str = Field(description="Seletor CSS para a área de conteúdo principal da página.")
    navigation_selector: str = Field(description="Seletor CSS para links de navegação para outras páginas do site.")
    next_page_selector: Optional[str] = Field(default=None, description="Seletor CSS para o link da próxima página (em caso de paginação).")

# llm deve ser uma instância de ChatGoogleGenerativeAI ou similar
structured_llm = llm.with_structured_output(SiteStructure)

# Exemplo de prompt para análise de HTML
html_content = "<!DOCTYPE html><html><head>...</head><body><main>...</main><nav>...</nav></body></html>" # Conteúdo HTML da página
prompt_text = f"""
Analise o seguinte conteúdo HTML e identifique os seletores CSS para a área de conteúdo principal,
links de navegação internos e, se aplicável, o link para a próxima página de uma sequência.

HTML:
{html_content}

Responda usando a estrutura fornecida.
"""

response_structured = structured_llm.invoke(prompt_text)
# response_structured será uma instância de SiteStructure
print(f"Seletor de Conteúdo: {response_structured.content_selector}")
print(f"Seletor de Navegação: {response_structured.navigation_selector}")
```

**Usando com TypedDict ou JSON Schema (para streaming ou sem validação Pydantic):**
Se for necessário streaming ou se a validação Pydantic não for desejada, pode-se usar `TypedDict` ou um JSON Schema.

```python
from typing_extensions import Annotated, TypedDict

class SiteStructureDict(TypedDict):
    """Estrutura de um site para scraping."""
    content_selector: Annotated[str, ..., "Seletor CSS para a área de conteúdo principal."]
    navigation_selector: Annotated[str, ..., "Seletor CSS para links de navegação."]
    next_page_selector: Annotated[Optional[str], None, "Seletor CSS para próxima página."]

structured_llm_dict = llm.with_structured_output(SiteStructureDict)
# Invocação similar ao exemplo com Pydantic
# response_dict = structured_llm_dict.invoke(prompt_text)
# print(response_dict['content_selector'])
```

**Considerações para o Prompt de Análise de HTML:**
*   O prompt deve instruir claramente o LLM a identificar seletores CSS.
*   Fornecer o conteúdo HTML dentro do prompt.
*   Indicar que a resposta deve seguir o schema fornecido (implícito ao usar `.with_structured_output()`).
*   Para HTMLs muito longos, pode ser necessário truncar ou resumir o HTML antes de enviar ao LLM, dependendo do limite de tokens do modelo.

Referência para Saída Estruturada: [LangChain How-to: Structured Output](https://python.langchain.com/v0.2/docs/how_to/structured_output/)

## Observações Adicionais
*   A URL principal de referência para LangChain é `https://github.com/langchain-ai/langchain` e sua documentação em `https://python.langchain.com/`.
*   É importante verificar a versão mais recente da documentação e dos pacotes, pois LangChain evolui rapidamente.
*   A gestão de API keys deve ser feita de forma segura, preferencialmente através de variáveis de ambiente ou gerenciadores de segredos.
*   Para a tarefa específica de identificar seletores em um HTML, o prompt enviado ao LLM precisa ser bem elaborado, possivelmente com exemplos (few-shot prompting) se a estrutura do site for complexa ou variar muito.
*   A funcionalidade de "tool calling" dos modelos Gemini é a base para o `.with_structured_output()` funcionar bem.
```
