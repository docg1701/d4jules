---
id: task-VIS
title: "Gerar/Atualizar VISION.md com base no working-plan.md e análise do código existente"
type: documentation
status: backlog
priority: high
dependencies: []
parent_plan_objective_id: "Fase2.2" # Referenciando o passo da Fase 2
discovered_research_needed: []
assigned_to: Jules
created_by: Jules
created_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for timestamp
updated_at: YYYY-MM-DDTHH:MM:SSZ # Placeholder for timestamp
tags: ["documentation", "vision", "planning"]
description: |
  Analisar o `jules-flow/working-plan.md` atual e, se aplicável, o código existente no repositório (especialmente se for uma atualização e não um projeto do zero). Com base nisso, gerar ou atualizar o arquivo `VISION.md` na raiz do projeto. Este arquivo deve detalhar:
  *   O objetivo geral do projeto (conforme `jules-flow/working-plan.md`).
  *   A arquitetura principal pretendida ou existente.
  *   Uma descrição das principais funcionalidades ou módulos que serão desenvolvidos/afetados, conforme inferido do `jules-flow/working-plan.md`.
  *   Quaisquer princípios de design ou tecnologias chave mencionadas ou implícitas no `jules-flow/working-plan.md`.
  *   Os principais fluxos de interação ou dados esperados.
  O `VISION.md` servirá como um documento de referência de alto nível para guiar o desenvolvimento subsequente.

# Não modificar esta seção manualmente. Jules irá preenchê-la.
# ---------------------------------------------------------------
# RELATÓRIO DE EXECUÇÃO (Preenchido por Jules ao concluir/falhar)
# ---------------------------------------------------------------
# outcome: success | failure
# outcome_reason: ""
# start_time: YYYY-MM-DDTHH:MM:SSZ
# end_time: YYYY-MM-DDTHH:MM:SSZ
# duration_minutes: 0
# files_modified:
#   - VISION.md
# reference_documents_consulted:
#   - jules-flow/working-plan.md
# execution_details: |
#   O arquivo VISION.md foi gerado na raiz do projeto com base no working-plan.md.
# ---------------------------------------------------------------
---

## Arquivos Relevantes (Escopo da Tarefa)
* `jules-flow/working-plan.md` (leitura)
* `VISION.md` (criação/atualização na raiz do projeto)
* Potenciais diretórios de código fonte para análise contextual (ex: `src/`, `app/`, ou `d4jules/` se já existir).

## Critérios de Aceitação
1. Um arquivo `VISION.md` é criado/atualizado na raiz do projeto.
2. O `VISION.md` contém as seções descritas: objetivo geral, arquitetura, funcionalidades/módulos, princípios/tecnologias, fluxos de interação/dados.

## Observações Adicionais
Como este é o início do projeto, o `VISION.md` será gerado do zero com base no `working-plan.md`. Não há código existente para analisar neste momento.
```
