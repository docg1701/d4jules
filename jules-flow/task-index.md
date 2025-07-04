# Índice de Tarefas Jules-Flow

| ID da Tarefa | Título | Tipo | Status | Prioridade | Dependências | Atribuído |
|--------------|--------|------|--------|------------|--------------|-----------|
| task-DOC01   | Atualizar Documentação do Projeto Pós-Implementação | documentation | done        | high       | []           | Jules     |
| task-R01     | Refatorar Crawler para Integrar Lógica de Scraping Completa | refactor | done        | high       | []           | Jules     |
| task-R02     | Implementar Controle de Profundidade (max_depth) no Crawler | refactor | done        | medium     | ["task-R01"] | Jules     |
| task-R03     | Melhorar Tratamento de Erros na Orquestração de Scraping | refactor | done        | medium     | ["task-R01"] | Jules     |
| task-R04     | Implementar Logging Estruturado em toda a Aplicação | refactor | done        | low        | ["task-R01"] | Jules     |
| task-FIX01   | Corrigir/Completar Exportações em src/core/__init__.py | fix      | done        | low        | []           | Jules     |
| task-R05     | Refatorar start.sh para Usar 'python -m src.scraper_cli' | refactor | done        | low        | []           | Jules     |
