# d4jules

![d4jules Project Icon](d4jules.webp)

**d4jules** é uma ferramenta de linha de comando (CLI) em Python projetada para analisar e realizar scraping de sites de documentação técnica. Utilizando Modelos de Linguagem Grandes (LLMs) como o Google Gemini, a ferramenta identifica autonomamente a estrutura de conteúdo e navegação das páginas, extrai as informações relevantes, converte-as para Markdown e as salva localmente. O objetivo é criar uma base de conhecimento estruturada para facilitar consultas por agentes de IA ou para referência pessoal.

## Funcionalidades Principais

*   **Análise Dinâmica de HTML:** Utiliza LLM (Google Gemini via LangChain) para identificar seletores CSS cruciais para conteúdo principal e links de navegação em páginas web.
*   **Crawling Automatizado:** Percorre sites de documentação de forma autônoma, seguindo os links de navegação identificados.
*   **Conversão para Markdown:** Transforma o conteúdo HTML relevante extraído em arquivos Markdown limpos e estruturados.
*   **Gerenciamento Eficiente de URLs:** Mantém uma fila de URLs a visitar e um registro de URLs já processadas para evitar trabalho redundante e loops de navegação.
*   **Configuração Centralizada:** Permite fácil configuração de chaves de API, modelos de LLM e outros parâmetros através de um arquivo `config/config.ini`.
*   **Inicialização Simplificada:** Inclui um script `start.sh` que automatiza a criação/ativação do ambiente virtual, atualização do repositório, instalação de dependências e execução da aplicação.
*   **Saída Organizada:** Salva os arquivos Markdown gerados no diretório `output/`, seguindo uma nomeclatura baseada na URL de origem.

## Pré-requisitos

Para executar o `d4jules`, você precisará ter os seguintes softwares instalados em seu sistema:

*   **Python 3** (idealmente 3.10 ou superior)
*   **pip** (gerenciador de pacotes Python, geralmente incluído com Python)
*   **python3-venv** (para criar ambientes virtuais Python; ex: `sudo apt-get install python3-venv` em Debian/Ubuntu)
*   **git** (para clonar o repositório e para a funcionalidade de `git pull` no `start.sh`)

O script `jules_bootstrap.sh` (se fornecido e utilizado para configurar o ambiente da VM) geralmente cuida da instalação dessas dependências de sistema.

## Configuração

Antes de executar a aplicação, você precisa configurar sua chave de API do Google AI.

1.  **Crie o arquivo de configuração:**
    Copie o arquivo de modelo `config/config.ini.template` para um novo arquivo chamado `config/config.ini`.
    ```bash
    cp config/config.ini.template config/config.ini
    ```

2.  **Edite `config/config.ini`:**
    Abra o arquivo `config/config.ini` em um editor de texto e preencha os seguintes campos:

    *   Na seção `[GOOGLE_AI]`:
        *   `API_KEY`: Substitua `YOUR_GOOGLE_AI_API_KEY_HERE` pela sua chave de API real do Google AI Studio.

    *   Na seção `[LLM]`:
        *   `MODEL_NAME`: O padrão é `gemini-1.5-flash-latest`. Você pode alterar para outro modelo compatível se desejar (ex: `gemini-1.5-pro-latest`). Certifique-se de que o modelo escolhido suporta as funcionalidades necessárias (como "tool calling" ou saída estruturada, dependendo da implementação do `analyzer.py`).

    *   Na seção `[CRAWLER_LIMITS]` (opcional, mas recomendada):
        *   `MAX_PAGES`: Número máximo de páginas a serem processadas em uma execução (ex: `100`).
        *   `MAX_DEPTH`: Profundidade máxima de crawling a partir da URL inicial (ex: `5`).

    Exemplo de `config/config.ini` (não comite este arquivo com sua chave real!):
    ```ini
    [GOOGLE_AI]
    API_KEY = SUA_CHAVE_DE_API_REAL_AQUI

    [LLM]
    MODEL_NAME = gemini-1.5-flash-latest

    [SCRAPER]
    # Placeholder for future scraper-specific settings...

    [CRAWLER_LIMITS]
    MAX_PAGES = 100
    MAX_DEPTH = 5
    ```

## Como Executar

O projeto inclui um script `start.sh` para facilitar a configuração do ambiente e a execução da aplicação.

1.  **Torne o script executável (se ainda não for):**
    ```bash
    chmod +x start.sh
    ```

2.  **Execute o script:**
    ```bash
    ./start.sh
    ```

O script `start.sh` realizará as seguintes ações:
*   Verificará a existência de um ambiente virtual Python chamado `.venv`. Se não existir, ele será criado.
*   Ativará o ambiente virtual.
*   Tentará atualizar o repositório local com `git pull`.
*   Atualizará `pip` para a versão mais recente dentro do ambiente virtual.
*   Instalará todas as dependências Python listadas no arquivo `requirements.txt`.
    Finalmente, executará a aplicação principal `src/scraper_cli.py` (como módulo: `python -m src.scraper_cli`).

Após a execução, o `src/scraper_cli.py` solicitará a URL do site de documentação a ser processado e iniciará o crawling conforme configurado.

## Estrutura do Projeto

```
.
├── .gitignore
├── AGENTS.md
├── README.md
├── VISION.md
├── config/                 # Arquivos de configuração
│   ├── config.ini.template
│   └── .gitignore          # Para ignorar config.ini
├── d4jules.webp
├── docs/                   # Documentação adicional do projeto
│   └── .gitkeep
├── jules-flow/             # Arquivos de gerenciamento de fluxo para Jules (você!)
├── jules_bootstrap.sh
├── output/                 # Saída gerada pelo scraper (ex: arquivos Markdown)
│   └── .gitkeep
├── requirements.txt        # Dependências Python
├── src/                    # Código fonte principal
│   ├── __init__.py         # Torna src um pacote Python
│   ├── scraper_cli.py      # Ponto de entrada da CLI (executado como módulo)
│   └── core/               # Módulos do núcleo da aplicação
│       ├── __init__.py     # Torna core um sub-pacote
│       ├── analyzer.py     # Análise de HTML com LLM
│       ├── config_loader.py# Carregamento de configuração
│       ├── crawler.py      # Lógica de crawling e gerenciamento de fila
│       ├── parser.py       # Parsing de HTML com BeautifulSoup
│       └── writer.py       # Conversão para Markdown e escrita de arquivos
├── start.sh                # Script de inicialização, setup de ambiente e execução
└── tests/                  # Testes unitários e de integração
    ├── __init__.py
    ├── .gitkeep
    └── core/               # Testes para os módulos do núcleo
        ├── __init__.py
        └── .gitkeep
```

## Tecnologias Utilizadas

*   **Python 3**
*   **LangChain (Python)**: Para orquestração e interação com LLMs. ([GitHub](https://github.com/langchain-ai/langchain))
*   **Google Gemini API (Python SDK)**: Modelo de linguagem para análise de HTML. ([GitHub](https://github.com/google/generative-ai-python))
*   **Beautiful Soup 4**: Para parsing de HTML. ([Documentation](https://beautiful-soup-4.readthedocs.io/en/latest/))
*   **html2text**: Para conversão de HTML para Markdown. ([GitHub](https://github.com/Alir3z4/html2text))
*   **Requests**: Para requisições HTTP.
*   **lxml**: Parser HTML eficiente usado com BeautifulSoup.
*   **unittest & unittest.mock**: Para escrita e execução de testes unitários em Python.
