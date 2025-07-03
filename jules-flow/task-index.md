# Índice de Tarefas Jules-Flow

| ID da Tarefa | Título | Tipo | Status | Prioridade | Dependências | Atribuído |
|--------------|--------|------|--------|------------|--------------|-----------|
| task-R01     | Pesquisa: LangChain (Python) | research | done | high | []           | Jules     |
| task-R02     | Pesquisa: Google Gemini API (Python SDK) | research | done | high | []           | Jules     |
| task-R03     | Pesquisa: Beautiful Soup | research | done | medium | []           | Jules     |
| task-R04     | Pesquisa: html2text      | research | done | medium | []           | Jules     |
| task-VIS     | Gerar/Atualizar VISION.md com base no working-plan.md e análise do código existente | documentation | done | high | []           | Jules     |
| task-D01     | Criar estrutura de diretórios base para d4jules | development | done | high | []           | Jules     |
| task-D02     | Implementar config.ini para d4jules | development | done | high | ["task-D01"] | Jules     |
| task-D03     | Criar requirements.txt para d4jules | development | done | high | []           | Jules     |
| task-D04     | Desenvolver verificação e criação de .venv em start.sh | development | done | medium | []           | Jules     |
| task-D05     | Adicionar ativação de venv, git pull e instalação de dependências ao start.sh | development | done | medium | ["task-D03", "task-D04"] | Jules     |
| task-D06     | Adicionar execução do scraper_cli.py ao start.sh | development | done | medium | ["task-D05"] | Jules     |
| task-T01     | Testar script start.sh   | test | done | medium | ["task-D06"] | Jules     |
| task-D07     | Implementar carregamento de config.ini em scraper_cli.py | development | done | high | ["task-D01", "task-D02"] | Jules     |
| task-D08     | Implementar solicitação de URL ao usuário em scraper_cli.py | development | done | medium | ["task-D07"] | Jules     |
| task-D09     | Implementar análise de HTML com LLM para extrair seletores | development | done | high | ["task-D07", "task-R01", "task-R02"] | Jules     |
| task-D10     | Implementar gerenciamento de fila de URLs e controle de visitas | development | done | medium | []           | Jules     |
| task-D11     | Implementar extração de conteúdo e links com BeautifulSoup | development | done | medium | ["task-R03"] | Jules     |
| task-D12     | Implementar conversão para Markdown e salvamento de arquivos | development | done | medium | ["task-R04", "task-D01"] | Jules     |
| task-D13     | Implementar lógica principal de orquestração do crawling | development | done | high | ["task-D09", "task-D10", "task-D11", "task-D12"] | Jules     |
| task-T02     | Testar funcionalidade completa do scraper_cli.py | test | done | high | ["task-D01", "task-D07", "task-D08", "task-D13"] | Jules     |
| task-T03     | Testes para a task-D01: Verificação da estrutura de diretórios | test | done | medium | ["task-D01"] | Jules     |
| task-T04     | Testes para a task-D02: Verificação dos arquivos de configuração | test | done | medium | ["task-D02"] | Jules     |
| task-T05     | Testes para a task-D03: Verificação do arquivo requirements.txt | test | done | medium | ["task-D03"] | Jules     |
| task-T06     | Testes para a task-D07: Carregamento de Configuração (REFAZER) | test | backlog | high | ["task-D07"] | Jules     |
| task-T07     | Testes para a task-D09: Análise de HTML com LLM para Extração de Seletores (REFAZER) | test | backlog | high | ["task-D09"] | Jules     |
| task-T08     | Testes para a task-D04: Verificação e criação de .venv em start.sh | test | done | medium | ["task-D04"] | Jules     |
| task-T09     | Testes para a task-D05: Ativação de venv e instalação de dependências em start.sh | test | done | medium | ["task-D05"] | Jules     |
| task-T10     | Testes para a task-D06: Execução de scraper_cli.py em start.sh | test | done | medium | ["task-D06"] | Jules     |
| task-T11     | Testes para a task-D08: Solicitação de URL ao usuário em scraper_cli.py | test | done | medium | ["task-D08"] | Jules     |
| task-FIX01   | Investigate and Restore Missing d4jules/src/core/crawler.py | fix | done | high | ["task-D10"] | Jules     |
| task-T12     | Testes para a task-D10: Gerenciamento de Fila de URLs e Controle de Visitas (REFAZER) | test | backlog | medium | ["task-D10", "task-FIX01"] | Jules     |
| task-FIX02   | Investigate and Restore Missing d4jules/src/core/parser.py | fix | done | high | ["task-D11"] | Jules     |
| task-T13     | Testes para a task-D11: Implementar extração de conteúdo e links com BeautifulSoup (REFAZER) | test | backlog | medium | ["task-D11", "task-FIX02"] | Jules     |
| task-T14     | Testes para a task-D12: Implementar conversão para Markdown e salvamento de arquivos | test | backlog | medium | ["task-D12"] | Jules     |
| task-T15     | Testes para a task-D13: Implementar lógica principal de orquestração do crawling | test | done | high | ["task-D13"] | Jules     |
| task-DOC01   | Criar README.md para d4jules | documentation | done | medium | ["task-D02", "task-D06"] | Jules     |
| task-DOC02   | Adicionar seção de Referências ao README.md | documentation | backlog | low | ["task-DOC01"] | Jules     |
