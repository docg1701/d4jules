# VISION.md - d4jules

## 1. Objetivo Geral do Projeto

O projeto **d4jules** visa criar uma ferramenta de linha de comando (CLI) em Python capaz de realizar o scraping completo de sites de documentação técnica. A ferramenta utilizará um Modelo de Linguagem Grande (LLM) do Google (ex: Gemini) para analisar a estrutura HTML das páginas, identificar seções de conteúdo principal e links de navegação relevantes. Após a análise, a ferramenta fará o crawling do site, extraindo o conteúdo de cada página, convertendo-o para o formato Markdown e salvando-o localmente. O objetivo final é gerar uma base de conhecimento estruturada e local, otimizada para consulta e utilização por agentes de Inteligência Artificial.

## 2. Arquitetura Principal

A arquitetura do `d4jules` será modular, organizada da seguinte forma:

*   **Interface de Linha de Comando (`scraper_cli.py`):** Ponto de entrada da aplicação, responsável pela interação com o usuário (coleta da URL inicial) e orquestração geral do processo.
*   **Módulo de Configuração (`d4jules/config/`):** Gerenciará as configurações da aplicação, como API keys e parâmetros do LLM, através de um arquivo `config.ini`. (Nota: O diretório `d4jules/config/` será criado em uma tarefa futura, `task-D02`).
*   **Núcleo de Processamento (`d4jules/src/core/`):**
    *   `analyzer.py` (ou similar): Responsável por interagir com o LLM (via LangChain) para analisar o HTML e extrair seletores CSS para conteúdo e navegação.
    *   `crawler.py` (ou similar): Gerenciará a fila de URLs, fará as requisições HTTP para baixar as páginas.
    *   `parser.py` (ou similar): Utilizará bibliotecas como BeautifulSoup para parsear o HTML bruto e extrair texto e links com base nos seletores fornecidos pelo `analyzer`.
    *   `writer.py` (ou similar): Converterá o conteúdo HTML extraído para Markdown (usando html2text) e salvará no sistema de arquivos.
*   **Utilitários (`d4jules/src/utils/`):** Contém funções auxiliares, como logging, manipulação de arquivos, etc.
*   **Saída de Dados (`d4jules/output/`):** Diretório padrão para armazenar os arquivos Markdown gerados e, potencialmente, os HTMLs brutos para referência.
    *   `d4jules/output/markdown/`
    *   `d4jules/output/raw_html/`
    (Nota: A subestrutura de `output/` será definida/refinada conforme a implementação).
*   **Logs (`d4jules/logs/`):** Para armazenar logs da execução da aplicação. (Nota: O diretório `d4jules/logs/` será criado em uma tarefa futura).
*   **Testes (`tests/`):** Contém os testes unitários e de integração para garantir a qualidade e o correto funcionamento da aplicação.
*   **Documentação (`docs/`):** Para documentação adicional do projeto, se necessário, além do `README.md`.
*   **Script de Automação (`start.sh`):** Facilitará a configuração do ambiente (criação de venv, instalação de dependências) e a execução da aplicação.

## 3. Principais Funcionalidades/Módulos

Conforme o `jules-flow/working-plan.md` e a lista de tarefas, as principais funcionalidades e módulos incluem:

1.  **Configuração Inicial e Estrutura do Projeto:**
    *   Criação da estrutura de diretórios (conforme `task-D01`).
    *   Implementação do `config.ini` para API keys e configurações do LLM (`task-D02`).
    *   Criação do `requirements.txt` (`task-D03`).
2.  **Script de Automação (`start.sh`):**
    *   Verificação e criação de ambiente virtual (`.venv`) (`task-D04`).
    *   Ativação do venv, `git pull`, instalação de dependências (`task-D05`).
    *   Execução do `scraper_cli.py` (`task-D06`).
    *   Testes do script `start.sh` (`task-T01`).
3.  **Aplicação Principal (`scraper_cli.py`):**
    *   Carregamento de `config.ini` (`task-D07`).
    *   Solicitação de URL ao usuário (`task-D08`).
    *   Análise de HTML com LLM para extrair seletores (usando LangChain e Gemini) (`task-D09`).
    *   Gerenciamento de fila de URLs e controle de visitas (evitar loops, revisitas desnecessárias) (`task-D10`).
    *   Extração de conteúdo e links com BeautifulSoup (baseado nos seletores do LLM) (`task-D11`).
    *   Conversão para Markdown (html2text) e salvamento de arquivos (`task-D12`).
    *   Lógica principal de orquestração do crawling, integrando os módulos acima (`task-D13`).
    *   Testes da funcionalidade completa do `scraper_cli.py` (`task-T02`).
4.  **Documentação do Projeto:**
    *   Criação do `README.md` (`task-DOC01`).
    *   Adição da seção de Referências ao `README.md` (`task-DOC02`).

## 4. Princípios de Design e Tecnologias Chave

*   **Modularidade:** O código será organizado em módulos com responsabilidades claras (análise, crawling, parsing, escrita).
*   **Configurabilidade:** As configurações sensíveis (API keys) e parâmetros do LLM serão externalizados em um arquivo `config.ini`.
*   **Uso de LLM para Análise Estrutural:** A principal inovação é o uso do LLM (Google Gemini) para interpretar a estrutura do HTML e identificar dinamicamente os seletores de conteúdo e navegação, em vez de depender de seletores fixos ou regras manuais.
*   **Scraping Robusto e Respeitoso:** Implementar mecanismos para gerenciar a fila de URLs, controlar a frequência de requisições (a ser considerado) e lidar com possíveis erros.
*   **Saída em Markdown:** O formato Markdown é escolhido por ser leve, legível e facilmente processável por outras ferramentas de IA.
*   **Tecnologias Principais:**
    *   **Python:** Linguagem de desenvolvimento principal.
    *   **LangChain:** Para orquestrar a interação com o LLM Google Gemini.
    *   **Google Gemini API (Python SDK):** Para acesso direto ao LLM Gemini.
    *   **BeautifulSoup4:** Para parsing de HTML e extração de dados.
    *   **html2text:** Para converter conteúdo HTML para Markdown.
    *   **Requests:** Para realizar requisições HTTP. (Ou `httpx` para assincronia, se decidido posteriormente).

## 5. Principais Fluxos de Interação e Dados

1.  **Inicialização:**
    *   Usuário executa `start.sh`.
    *   Script configura o ambiente (venv, dependências).
    *   Script executa `python scraper_cli.py`.
2.  **Coleta da URL Inicial:**
    *   `scraper_cli.py` carrega `config.ini`.
    *   `scraper_cli.py` solicita ao usuário a URL do site de documentação a ser processado.
3.  **Análise da Página Inicial (e subsequentes, se necessário para navegação):**
    *   Aplicaçãorealiza o download do HTML da URL fornecida.
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
