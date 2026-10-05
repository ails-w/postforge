# Handoff — postforge

> Estado MUTABLE. Se sobreescribe al iniciar/cerrar sesión. Última actualización: 2026-10-05.

## Fase activa

**Fase 1 — EN PROGRESO** (Ingesta + índice; rama `dev`).
**Fase 0 — COMPLETADA Y VERIFICADA** (scaffold, research, knowledge, prompts, código base y spikes). CI en verde en el primer push (run #36323272674, 2026-09-27).

## Próximo paso

1. **Feature 1.1:** scanner git-aware (`ingest/scanner.py`, con fallback sin git) → test RED primero.
2. Features 1.2–1.5: chunkers (markdown y código), esquema SQLite + FTS5, CLI `index`/`search`.
3. Al cerrar la fase: PR `dev → main` (gates `lint`/`test`/`build`).

## Decisiones recientes

- Stack v1: Python 3.12 + uv (ADR-001); TUI en C# como upgrade path.
- LLM vía `opencode run --format json` (ADR-002); contrato JSONL + `sessionID` verificado (ADR-005).
- RAG por proyecto y `knowledge/` separado (ADR-003).
- Embeddings: MiniLM multilingüe, con fusión léxica obligatoria (ADR-004).
- Modelos: `deepseek-v4.1-flash` (map) + `glm-5.3` (redacción); corrida < USD 0,02 (ADR-005).
- Interacción: batch + `refine` (chat que reusa `sessionID`).

## Estado del repo (apertura Fase 1)

- CI en 3 gates: `lint`, `test`, `build` (run verde en `main`).
- `main` protegida por el ruleset `protect-main`: PR + 3 checks + sin force-push ni borrado.
- Trabajo de la fase en `dev` (creada desde `main`, trackea `origin/dev`).
- Python 3.12.14 con uv; 15 tests verdes; ruff limpio.
- `projects.yaml` registra `focusguard` y `focusblock`.
- Guías: `docs/learning/phase-01-ingest.md` (conceptos) + `docs/progress-log/phase-01-ingest.md` (log).

## Riesgos

- El token de `gh` no tiene scope `workflow`: los cambios a `.github/workflows/` requieren push por SSH del usuario.
- CI en verde en `main` (setup-uv + `uv sync --frozen`); tras la protección, solo llega por PR.
- Cuota de la suscripción → mitigado: tier barato para el map; modelos configurables.
- `mmdc` puede requerir Chromium headless → verificar en Fase 4.
- Secretos: nada de la auth de OpenCode entra al repo. Opcional antes del push público: `gitleaks` como pre-commit.

## Repo

```bash
# Remoto: https://github.com/ails-w/postforge (público)
# origin: fetch por SSH, push por HTTPS (token de gh)
# Ramas: main (protegida por ruleset protect-main) + dev

# cerrar una fase: PR de dev a main (exige lint + test + build)
gh pr create --base main --head dev --fill
```
