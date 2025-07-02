# Índice de Tarefas Jules-Flow

| ID da Tarefa | Título | Tipo | Status | Prioridade | Dependências | Atribuído |
|--------------|--------|------|--------|------------|--------------|-----------|
| task-R01     | Pesquisa: LangChain (Python) | research | backlog | high | []           | Jules     |
| task-R02     | Pesquisa: Google Gemini API (Python SDK) | research | backlog | high | []           | Jules     |
| task-R03     | Pesquisa: Beautiful Soup | research | backlog | medium | []           | Jules     |
| task-R04     | Pesquisa: html2text      | research | backlog | medium | []           | Jules     |
| task-VIS     | Gerar/Atualizar VISION.md com base no working-plan.md e análise do código existente | documentation | backlog | high | []           | Jules     |
| task-D01     | Criar estrutura de diretórios base para d4jules | development | backlog | high | []           | Jules     |
| task-D02     | Implementar config.ini para d4jules | development | backlog | high | ["task-D01"] | Jules     |
| task-D03     | Criar requirements.txt para d4jules | development | backlog | high | []           | Jules     |
| task-D04     | Desenvolver verificação e criação de .venv em start.sh | development | backlog | medium | []           | Jules     |
| task-D05     | Adicionar ativação de venv, git pull e instalação de dependências ao start.sh | development | backlog | medium | ["task-D03", "task-D04"] | Jules     |
| task-D06     | Adicionar execução do scraper_cli.py ao start.sh | development | backlog | medium | ["task-D05"] | Jules     |
| task-T01     | Testar script start.sh   | test | backlog | medium | ["task-D06"] | Jules     |
| task-D07     | Implementar carregamento de config.ini em scraper_cli.py | development | backlog | high | ["task-D01", "task-D02"] | Jules     |
| task-D08     | Implementar solicitação de URL ao usuário em scraper_cli.py | development | backlog | medium | ["task-D07"] | Jules     |
| task-D09     | Implementar análise de HTML com LLM para extrair seletores | development | backlog | high | ["task-D07", "task-R01", "task-R02"] | Jules     |
| task-D10     | Implementar gerenciamento de fila de URLs e controle de visitas | development | backlog | medium | []           | Jules     |
| task-D11     | Implementar extração de conteúdo e links com BeautifulSoup | development | backlog | medium | ["task-R03"] | Jules     |
| task-D12     | Implementar conversão para Markdown e salvamento de arquivos | development | backlog | medium | ["task-R04", "task-D01"] | Jules     |
| task-D13     | Implementar lógica principal de orquestração do crawling | development | backlog | high | ["task-D09", "task-D10", "task-D11", "task-D12"] | Jules     |
| task-T02     | Testar funcionalidade completa do scraper_cli.py | test | backlog | high | ["task-D01", "task-D07", "task-D08", "task-D13"] | Jules     |
| task-DOC01   | Criar README.md para d4jules | documentation | backlog | medium | ["task-D02", "task-D06"] | Jules     |
| task-DOC02   | Adicionar seção de Referências ao README.md | documentation | backlog | low | ["task-DOC01"] | Jules     |
