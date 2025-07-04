# VISION.md - d4jules

## 1. Objetivo Geral do Projeto

O projeto **d4jules** visa criar uma ferramenta de linha de comando (CLI) em Python capaz de realizar o scraping completo de sites de documentação técnica. A ferramenta utilizará um Modelo de Linguagem Grande (LLM) do Google (ex: Gemini) para analisar a estrutura HTML das páginas, identificar seções de conteúdo principal e links de navegação relevantes. Após a análise, a ferramenta fará o crawling do site, extraindo o conteúdo de cada página, convertendo-o para o formato Markdown e salvando-o localmente. O objetivo final é gerar uma base de conhecimento estruturada e local, otimizada para consulta e utilização por agentes de Inteligência Artificial.

## 2. Arquitetura Principal

A arquitetura do `d4jules` será modular, organizada da seguinte forma:

*   **Interface de Linha de Comando (`src/scraper_cli.py`):** Ponto de entrada da aplicação, executado como módulo (`python -m src.scraper_cli`). Responsável pela interação com o usuário (coleta da URL inicial, etc.) e orquestração geral do processo de scraping.
*   **Módulo de Configuração (`config/`):** Localizado na raiz do projeto, gerencia as configurações da aplicação (API keys, parâmetros do LLM, limites de crawling) através de um arquivo `config.ini`. O `src/core/config_loader.py` é responsável por carregar estas configurações.
*   **Núcleo de Processamento (`src/core/`):** Contém os módulos centrais da lógica de scraping:
    *   `analyzer.py`: Interage com o LLM (Google Gemini via LangChain) para analisar o HTML de uma URL e extrair seletores CSS para conteúdo principal e links de navegação.
    *   `crawler.py`: Gerencia a fila de URLs a visitar, controla URLs já visitadas, respeita limites de profundidade e número de páginas, e orquestra o processo de download, análise, parsing e escrita para cada URL.
    *   `parser.py`: Utiliza BeautifulSoup para parsear o HTML bruto, extrair o conteúdo principal e os links de navegação com base nos seletores fornecidos pelo `analyzer.py`.
    *   `writer.py`: Converte o conteúdo HTML extraído para o formato Markdown (usando `html2text`) e o salva no sistema de arquivos dentro do diretório `output/`.
*   **Utilitários (`src/utils/`):** Diretório planejado para funções auxiliares (logging, manipulação de arquivos, etc.). *Nota: Atualmente, este diretório pode não estar populado ou pode ter sido integrado a outros módulos se a complexidade não justificou sua separação.*
*   **Saída de Dados (`output/`):** Diretório padrão na raiz do projeto onde os arquivos Markdown gerados são armazenados. A nomeação dos arquivos é baseada na URL de origem.
*   **Logs (`logs/`):** Diretório planejado na raiz para armazenar logs da execução da aplicação. *Nota: A implementação detalhada de logging e a criação deste diretório podem ser tarefas futuras.*
*   **Testes (`tests/`):** Localizado na raiz, contém os testes unitários e de integração.
    *   `tests/core/`: Contém testes específicos para os módulos em `src/core/`.
*   **Documentação (`docs/`):** Para documentação adicional do projeto (guias, arquitetura detalhada, etc.), complementando o `README.md` e `VISION.md`.
*   **Script de Automação (`start.sh`):** Localizado na raiz, facilita a configuração do ambiente (criação e ativação de ambiente virtual `.venv`, instalação de dependências do `requirements.txt`) e a execução da aplicação principal.

## 3. Principais Funcionalidades/Módulos (Implementadas)

Com base no ciclo de desenvolvimento concluído (referenciado pelo `jules-flow/final-reports/final-report-*.md`), as seguintes funcionalidades e módulos foram implementados e testados:

1.  **Configuração Inicial e Estrutura do Projeto:**
    *   Criação e refatoração da estrutura de diretórios do projeto.
    *   Implementação do sistema de configuração via `config/config.ini` e `src/core/config_loader.py` (para API keys, modelo LLM, limites de crawling).
    *   Criação do `requirements.txt` com todas as dependências necessárias.
2.  **Script de Automação (`start.sh`):**
    *   Verificação e criação de ambiente virtual (`.venv`).
    *   Ativação do venv, `git pull` para atualizações, instalação/atualização de dependências.
    *   Execução do `src/scraper_cli.py` como módulo.
    *   Testes abrangentes do script `start.sh`.
3.  **Aplicação Principal (`src/scraper_cli.py`) e Núcleo de Scraping (`src/core/`):**
    *   Carregamento da configuração, incluindo limites de crawling.
    *   Solicitação interativa da URL inicial ao usuário.
    *   **Análise de HTML com LLM (`analyzer.py`):** Extração de seletores CSS (conteúdo, navegação) de URLs usando Google Gemini via LangChain, com tratamento de erros.
    *   **Gerenciamento de Crawling (`crawler.py`):** Lógica robusta para gerenciar a fila de URLs, controlar URLs visitadas, profundidade, número máximo de páginas e orquestrar o ciclo de scraping por URL.
    *   **Parsing de HTML (`parser.py`):** Extração de conteúdo e links de páginas HTML usando BeautifulSoup, com base nos seletores identificados.
    *   **Escrita de Conteúdo (`writer.py`):** Conversão do conteúdo HTML extraído para Markdown (usando `html2text`) e salvamento em arquivos no diretório `output/`.
    *   Lógica de orquestração principal no `scraper_cli.py` integrando todos os módulos do núcleo.
    *   Testes unitários para todos os módulos do núcleo (`config_loader`, `analyzer`, `crawler`, `parser`, `writer`) e testes E2E (com mocks) para o `scraper_cli.py`.
4.  **Documentação Inicial do Projeto:**
    *   Criação e atualização do `README.md` com instruções de setup, uso e visão geral.
    *   Criação deste `VISION.md`.

## 4. Princípios de Design e Tecnologias Chave

*   **Modularidade:** O código será organizado em módulos com responsabilidades claras (análise, crawling, parsing, escrita).
*   **Configurabilidade:** As configurações sensíveis (API keys) e parâmetros do LLM serão externalizados em um arquivo `config.ini`.
*   **Uso de LLM para Análise Estrutural:** A principal inovação é o uso do LLM (Google Gemini) para interpretar a estrutura do HTML e identificar dinamicamente os seletores de conteúdo e navegação, em vez de depender de seletores fixos ou regras manuais.
*   **Scraping Robusto e Respeitoso:** Implementar mecanismos para gerenciar a fila de URLs, controlar a frequência de requisições (a ser considerado) e lidar com possíveis erros.
*   **Saída em Markdown:** O formato Markdown é escolhido por ser leve, legível e facilmente processável por outras ferramentas de IA.
*   **Tecnologias Principais:**
    *   **Python 3:** Linguagem de desenvolvimento principal.
    *   **LangChain (Python SDK):** Para orquestrar a interação com o LLM Google Gemini, incluindo gerenciamento de prompts e parsing de saída estruturada.
    *   **Google Gemini API (Python SDK):** Para acesso direto ao LLM Gemini para análise de HTML.
    *   **BeautifulSoup4 (com lxml):** Para parsing eficiente de HTML e extração de dados baseada em seletores.
    *   **html2text:** Para converter conteúdo HTML limpo para o formato Markdown.
    *   **Requests:** Para realizar requisições HTTP para download de páginas web.
    *   **configparser:** Para ler e gerenciar o arquivo de configuração `config.ini`.
    *   **unittest & unittest.mock:** Para desenvolvimento e execução de testes unitários.

## 5. Principais Fluxos de Interação e Dados

1.  **Inicialização via `start.sh`:**
    *   Usuário executa `./start.sh`.
    *   O script verifica/cria o ambiente virtual (`.venv`), o ativa, atualiza o repositório (`git pull`), instala/atualiza dependências (`pip install -r requirements.txt`).
    *   O script executa a aplicação principal: `python -m src.scraper_cli`.
2.  **Configuração e Coleta da URL Inicial (`src/scraper_cli.py`):**
    *   A aplicação carrega as configurações do `config/config.ini` (API Key, nome do modelo LLM, limites de crawling) usando `src/core/config_loader.py`.
    *   Solicita interativamente ao usuário a URL do site de documentação a ser processado.
3.  **Ciclo de Crawling (orquestrado por `src/core/crawler.py` e `src/scraper_cli.py`):**
    *   A URL inicial é adicionada a uma fila de URLs a visitar.
    *   Enquanto a fila não estiver vazia e os limites (páginas/profundidade) não forem atingidos:
        a.  Uma URL é retirada da fila.
        b.  **Análise com LLM (`src/core/analyzer.py`):** O HTML da URL é baixado (via `requests`). Esse HTML é enviado ao LLM (Gemini) para identificar seletores CSS para: área de conteúdo principal, links de navegação interna e, opcionalmente, link para "próxima página".
        c.  **Parsing (`src/core/parser.py`):** O HTML da página é novamente processado (ou o HTML já baixado é usado) com BeautifulSoup e os seletores obtidos para:
            i.  Extrair o elemento HTML do conteúdo principal.
            ii. Extrair todas as URLs de navegação interna e o link da "próxima página".
        d.  **Escrita (`src/core/writer.py`):** O HTML do conteúdo principal é convertido para Markdown e salvo em um arquivo local (ex: `output/nome_da_pagina.md`).
        e.  **Atualização da Fila:** Novas URLs de navegação válidas (mesmo domínio, não visitadas, dentro do limite de profundidade) são adicionadas à fila.
        f.  A URL processada é marcada como visitada.
4.  **Conclusão:**
    *   O processo continua até que a fila de URLs esteja vazia ou um dos limites de crawling (número de páginas ou profundidade) seja atingido.
    *   A aplicação informa ao usuário a conclusão do processo e a localização dos arquivos Markdown gerados em `output/`.

Este documento `VISION.md` servirá como um guia de alto nível e poderá ser atualizado conforme o projeto evolui e novas decisões são tomadas.
    *   O HTML é enviado para o LLM (Gemini via LangChain) com um prompt para identificar seletores CSS para:
        *   Área de conteúdo principal.
        *   Links de navegação internos do site (para outras páginas de documentação).
        *   (Opcional) Link para "próxima página" em caso de paginação de conteúdo.
    *   O LLM retorna os seletores em formato JSON estruturado.
4.  **Crawling e Extração:**
    *   Uma fila de URLs a visitar é iniciada com a URL base.
    *   Para cada URL na fila:
        *   Se a URL já não foi visitada:
            *   Baixar o HTML da página.
            *   Usar BeautifulSoup e os seletores (identificados pelo LLM ou herdados/refinados) para:
                *   Extrair a seção de conteúdo principal.
                *   Extrair novos links de navegação interna e adicioná-los à fila (se ainda não visitados/processados).
            *   Converter o conteúdo principal extraído para Markdown usando `html2text`.
            *   Salvar o Markdown em um arquivo local (ex: `output/markdown/nome_da_pagina.md`).
            *   (Opcional) Salvar o HTML bruto em `output/raw_html/` para referência.
            *   Marcar a URL como visitada.
5.  **Conclusão:**
    *   O processo continua até que a fila de URLs esteja vazia ou um limite definido seja atingido.
    *   A aplicação informa ao usuário a conclusão e a localização dos arquivos Markdown.

Este documento `VISION.md` servirá como um guia de alto nível e poderá ser atualizado conforme o projeto evolui e novas decisões são tomadas.
