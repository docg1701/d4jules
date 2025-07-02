---
# Plano de Trabalho para Jules
## Objetivo Geral
Criar uma ferramenta de linha de comando em Python chamada `d4jules`. A ferramenta irá interagir com o usuário para obter a URL de um site de documentação técnica, utilizará um modelo de linguagem (LLM) do Google, como o `gemini-1.5-flash-latest`, para analisar a estrutura do site e identificar as áreas de conteúdo e navegação, e então fará o scraping (crawling) de todo o site. O conteúdo de cada página será convertido para o formato Markdown e salvo localmente, criando uma base de conhecimento estruturada para consulta por agentes de IA. O projeto deve incluir um script de automação (`start.sh`) para configurar o ambiente e executar a aplicação.

## Passo a Passo da Execução para Jules
1.  **Estruturar o Projeto e a Configuração Inicial:**
    1. Crie a estrutura de diretórios base para o projeto `d4jules`.
    2. Implemente o arquivo de configuração `config.ini` com as seções `[GOOGLE_AI]` e `[LLM]` para permitir a configuração externa da API e do modelo.
    3. Crie o arquivo `requirements.txt` com as dependências: `langchain`, `google-generativeai`, `beautifulsoup4`, `html2text`, e `requests`.

2.  **Implementar o Script de Automação (`start.sh`):**
    1. Desenvolva um script de shell que verifique a existência de um ambiente virtual (`.venv`) e o crie se necessário.
    2. Adicione ao script os comandos para ativar o ambiente virtual, executar `git pull` para atualizar o código, e instalar as dependências do `requirements.txt`.
    3. O script deve finalizar executando a aplicação principal `python scraper_cli.py`.

3.  **Desenvolver o Script Principal (`scraper_cli.py`):**
    1. Implemente a lógica para carregar as configurações do `config.ini` na inicialização.
    2. Adicione o código para interagir com o usuário, solicitando a URL a ser processada.
    3. Implemente a função de análise com o LLM: baixar o HTML da URL inicial, enviá-lo via LangChain para o Gemini e extrair os seletores de conteúdo e navegação da resposta JSON.
    4. Desenvolva a lógica principal de crawling: gerenciar uma fila de URLs a visitar, extrair o conteúdo de cada página usando `BeautifulSoup`, convertê-lo para Markdown com `html2text`, e salvar os arquivos no diretório de saída.

4.  **Finalizar a Documentação:**
    1. Crie um arquivo `README.md` claro, explicando o propósito do `d4jules`, como preencher o `config.ini` e como executar o projeto com o script `start.sh`.
    2. Adicione uma seção de "Referências" no `README.md` com os links para a documentação das tecnologias utilizadas:
        1. **LangChain (Python):** `https://github.com/langchain-ai/langchain`
        2. **Google Gemini API (Python SDK):** `https://github.com/google/generative-ai-python`
        3. **Beautiful Soup:** `https://beautiful-soup-4.readthedocs.io/en/latest/`
        4. **html2text:** `https://github.com/Alir3z4/html2text`
---
