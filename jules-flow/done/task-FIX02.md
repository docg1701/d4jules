---
id: task-FIX02
title: "Consolidate Core Module Paths and Project Structure"
type: fix
status: backlog # Will be updated to in_progress in task-index.md
priority: high
dependencies: ["task-D11", "task-FIX01"] # Depends on core modules existing
parent_plan_objective_id: null # Corrective task
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: 2024-07-03T02:00:00Z # Placeholder
updated_at: 2024-07-03T02:00:00Z # Placeholder
tags: ["refactor", "structure", "core-functionality", "parser", "writer", "crawler"]
description: |
  The project structure initially had core modules and `scraper_cli.py` within a top-level `d4jules/` directory.
  This task documents the refactoring to move all application code (`src/`, `config/`, `output/`, `scraper_cli.py`, etc.) to the project root,
  eliminating the unnecessary `d4jules/` nesting for these components. `VISION.md` now reflects this flatter structure.

  **Actions Required (Reflecting Final State):**
  1.  **Ensure `parser.py`, `writer.py`, `crawler.py`, `config_loader.py`, `analyzer.py` are in `src/core/`.**
  2.  **Ensure `scraper_cli.py` is in the project root.**
  3.  **Ensure `config.ini.template` and related `.gitignore` are in `config/` at the project root.**
  4.  **Ensure `output/` directory is at the project root.**
  5.  **Ensure `tests/` directory is at the project root, with `tests/core/` for core module tests.**
  6.  **Update `src/core/__init__.py`**: Ensure it exports necessary functions/classes from all modules in `src/core/`.
  7.  **Verify Imports**: Perform basic import checks and review `scraper_cli.py` and all files in `tests/` for correct import paths (e.g., `from src.core import ...`).

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success
# outcome_reason: "Project structure refactored. Core files moved from 'd4jules/src/core/' to 'src/core/', 'scraper_cli.py' to root, 'config' to root, etc. The 'd4jules' directory for application code was removed. Import paths updated across the project. `analyzer.py` was recreated."
# start_time: 2024-07-03T02:05:00Z # Approximate (original FIX02 start)
# end_time: 2024-07-26T18:00:00Z # Approximate (end of full refactor described now)
# duration_minutes: 15 # (original FIX02) - Total refactor much longer.
# files_modified:
#   - src/core/parser.py
#   - src/core/writer.py
#   - src/core/crawler.py
#   - src/core/config_loader.py
#   - src/core/analyzer.py # Recreated
#   - src/core/__init__.py
#   - scraper_cli.py
#   - config/config.ini.template
#   - config/.gitignore
#   - tests/core/test_*.py (multiple files)
#   - tests/test_*.py (multiple files)
#   - VISION.md
#   - (Other task markdown files in jules-flow/done/)
# reference_documents_consulted:
#   - VISION.md (original and updated)
#   - Various *.md task files in jules-flow/
# execution_details: |
#   1. **Confirmed Final Directory Structure**: `src/core/` for core logic, `config/` for configuration, `output/` for results, `scraper_cli.py` in root.
#   2. **Moved/Verified Core Files**: Ensured all core Python modules (`parser.py`, `writer.py`, `crawler.py`, `config_loader.py`, `analyzer.py`) are located in `src/core/`. `analyzer.py` was recreated.
#   3. **Moved/Verified Other Components**: `scraper_cli.py` moved to root. `config/` and `output/` directories established at root.
#   4. **Removed Redundant `d4jules` Directory**: The top-level `d4jules/` directory (that previously held app code) was removed after its contents were relocated.
#   5. **Updated `src/core/__init__.py`**: Ensured it exports necessary components from modules within `src/core/`.
#   6. **Updated Import Paths**: All import statements in `scraper_cli.py`, `src/core/*` files (if any inter-dependencies), and all test files in `tests/` and `tests/core/` were updated to reflect the new structure (e.g., `from src.core.module import MyClass`). Default paths in code (e.g., to `config.ini`) were also updated.
#   7. **Documentation Updated**: `VISION.md` and relevant `jules-flow` task files were updated to reflect the new structure and paths.
#
#   Overall, the project structure has been significantly refactored for clarity and correctness according to `VISION.md`.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `src/core/parser.py`
* `src/core/writer.py`
* `src/core/crawler.py`
* `src/core/config_loader.py`
* `src/core/analyzer.py`
* `src/core/__init__.py`
* `scraper_cli.py`
* `config/`
* `output/`
* `tests/`
* `jules-flow/done/task-D11.md` (for reference)

## Critérios de Aceitação
1.  The directory `src/core/` is the sole location for `parser.py`, `writer.py`, `crawler.py`, `config_loader.py`, `analyzer.py`.
2.  `scraper_cli.py` is in the project root.
3.  `config/` and `output/` directories are at the project root.
4.  The old `d4jules/` directory (for application code) is removed.
5.  `src/core/__init__.py` correctly exports all necessary components.
6.  Basic import checks for all core modules pass.
7.  Key files like `scraper_cli.py` and all tests use correct import paths (e.g. `from src.core...`).
```
