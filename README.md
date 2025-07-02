# d4jules

![d4jules Project Icon](d4jules.webp)

**d4jules** é uma ferramenta de linha de comando (CLI) em Python projetada para analisar e realizar scraping de sites de documentação técnica. Utilizando Modelos de Linguagem Grandes (LLMs) como o Google Gemini, a ferramenta identifica autonomamente a estrutura de conteúdo e navegação das páginas, extrai as informações relevantes, converte-as para Markdown e as salva localmente. O objetivo é criar uma base de conhecimento estruturada para facilitar consultas por agentes de IA ou para referência pessoal.

## Funcionalidades Principais (Planejadas)

*   Análise de HTML com LLM para identificar seletores CSS de conteúdo e navegação.
*   Crawling automatizado de sites de documentação.
*   Conversão de conteúdo HTML para Markdown.
*   Gerenciamento de fila de URLs e controle de URLs já visitadas para evitar redundância e loops.
*   Configuração flexível através de um arquivo `config.ini`.
*   Script de inicialização (`start.sh`) para fácil configuração do ambiente e execução.

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
    Copie o arquivo de modelo `d4jules/config/config.ini.template` para um novo arquivo chamado `d4jules/config/config.ini`.
    ```bash
    cp d4jules/config/config.ini.template d4jules/config/config.ini
    ```

2.  **Edite `d4jules/config/config.ini`:**
    Abra o arquivo `d4jules/config/config.ini` em um editor de texto e preencha os seguintes campos:

    *   Na seção `[GOOGLE_AI]`:
        *   `API_KEY`: Substitua `YOUR_GOOGLE_AI_API_KEY_HERE` pela sua chave de API real do Google AI Studio.

    *   Na seção `[LLM]`:
        *   `MODEL_NAME`: O padrão é `gemini-1.5-flash-latest`. Você pode alterar para outro modelo compatível se desejar (ex: `gemini-1.5-pro-latest`). Certifique-se de que o modelo escolhido suporta as funcionalidades necessárias (como "tool calling" ou saída estruturada, dependendo da implementação do `analyzer.py`).

    Exemplo de `config.ini` preenchido (não comite este arquivo com sua chave real!):
    ```ini
    [GOOGLE_AI]
    API_KEY = SUA_CHAVE_DE_API_REAL_AQUI

    [LLM]
    MODEL_NAME = gemini-1.5-flash-latest

    [SCRAPER]
    # Placeholder for future scraper-specific settings...
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
*   Finalmente, executará a aplicação principal `d4jules/scraper_cli.py`.

Após a execução, o `scraper_cli.py` (atualmente em desenvolvimento) solicitará a URL do site de documentação a ser processado.

## Estrutura do Projeto (Simplificada)

```
.
├── d4jules/                # Pacote principal da aplicação
│   ├── __init__.py
│   ├── scraper_cli.py      # Ponto de entrada da CLI
│   ├── config/             # Arquivos de configuração
│   │   ├── config.ini.template
│   │   └── .gitignore      # Para ignorar config.ini
│   ├── src/                # Código fonte principal
│   │   ├── __init__.py
│   │   └── core/           # Módulos principais (analyzer, crawler, etc.)
│   │       ├── __init__.py
│   │       ├── analyzer.py
│   │       ├── config_loader.py
│   │       └── crawler.py
│   └── output/             # Saída gerada pelo scraper (ex: arquivos Markdown)
│       └── .gitkeep
├── tests/                  # Testes unitários e de integração
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_config_loader.py
├── .gitignore
├── jules-flow/             # Arquivos de gerenciamento de fluxo para Jules (você!)
├── requirements.txt        # Dependências Python
├── start.sh                # Script de inicialização e setup
└── VISION.md               # Documento de visão do projeto
```

## Tecnologias Utilizadas

*   **Python 3**
*   **LangChain**: Para orquestração e interação com LLMs.
*   **Google Gemini API**: Modelo de linguagem para análise de HTML.
*   **BeautifulSoup4**: Para parsing de HTML.
*   **html2text**: Para conversão de HTML para Markdown.
*   **Requests**: Para requisições HTTP.
