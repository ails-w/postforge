# Handoff — postforge

> Estado MUTABLE. Se sobreescribe al iniciar/cerrar sesión. Última actualización: 2026-10-05.

## Fase activa

**Fase 0 — COMPLETADA Y VERIFICADA** (scaffold, research, knowledge, prompts, código base y spikes). CI en verde en el primer push (run #36323272674, 2026-09-27).
**Próxima: Fase 1 — Ingesta + índice** (se abre en rama `dev`).

## Próximo paso

1. **Primer push:** crear el repo remoto y verificar el CI (comando en §Repo).
2. **Abrir Fase 1:** copiar `learning/template-phase.md` y `progress-log/template-phase.md` a `phase-01-ingest.*`; rama `dev`.
3. **Feature 1.1:** scanner git-aware (con fallback sin git) → test RED primero.

## Decisiones recientes

- Stack v1: Python 3.12 + uv (ADR-001); TUI en C# como upgrade path.
- LLM vía `opencode run --format json` (ADR-002); contrato JSONL + `sessionID` verificado (ADR-005).
- RAG por proyecto y `knowledge/` separado (ADR-003).
- Embeddings: MiniLM multilingüe, con fusión léxica obligatoria (ADR-004).
- Modelos: `deepseek-v4.1-flash` (map) + `glm-5.3` (redacción); corrida < USD 0,02 (ADR-005).
- Interacción: batch + `refine` (chat que reusa `sessionID`).

## Estado del repo (cierre Fase 0)

- `uv sync` OK con Python 3.12.14; `uv.lock` commiteado; 15 tests verdes; ruff limpio.
- CLI con 5 comandos como stubs; adaptador LLM probado contra la suscripción.
- `knowledge/` completo; `prompts/` con los 4 prompts del pipeline.
- Guías de aprendizaje: `docs/learning/uv.md` (transversal) + `docs/learning/phase-00-setup.md`.
- Historial de la fase: `docs/progress-log/phase-00-setup.md`.

## Riesgos

- CI verificado en el primer push: run #36323272674 completed/success (setup-uv + `uv sync --frozen`).
- Cuota de la suscripción → mitigado: tier barato para el map; modelos configurables.
- `mmdc` puede requerir Chromium headless → verificar en Fase 4.
- Secretos: nada de la auth de OpenCode entra al repo. Opcional antes del push público: `gitleaks` como pre-commit.

## Repo

```bash
gh repo create postforge --public --source=. --remote=origin \
  --description "Generate LinkedIn posts from a repository's real documentation (local RAG + OpenCode)"
git push -u origin main
# al abrir Fase 1:
git checkout -b dev && git push -u origin dev
```
