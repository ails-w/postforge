# Fase 1: Ingesta + índice — Log

> Log HISTÓRICO de la fase. Se acumula, no se borra.
> Estado actual → `docs/handoff.md` · Conceptos → `docs/learning/phase-01-ingest.md`

## Estado

**Estado**: En Progreso
**Última Actualización**: 2026-10-05 19:00

## Objetivos

- `postforge index <slug>` convierte un repo en un índice consultable.
- Chunking determinista con metadata (`archivo:línea`).
- `postforge search "<query>"` devuelve chunks con `archivo:línea`.
- Golden files del corpus baseline (`focusguard`, `focusblock`) en verde.

## Progreso

- [ ] Feature 1.1: Scanner git-aware (con fallback sin git)
- [ ] Feature 1.2: Chunker de markdown
- [ ] Feature 1.3: Chunker de código
- [ ] Feature 1.4: Esquema SQLite + FTS5
- [ ] Feature 1.5: CLI `index` y `search`

## Tareas Completadas

### 2026-10-05 — Kickoff de la fase

- **Descripción**: Apertura de Fase 1 en rama `dev` (regla del phase-plan). Documento de conceptos y log creados desde plantilla. Ramas y CI ya preparados.
- **Archivos**: `docs/learning/phase-01-ingest.md`, `docs/progress-log/phase-01-ingest.md`.
- **Tests**: — (sin código todavía).

## Decisiones

1. **Fase 1 trabaja en `dev`** — *por qué*: `main` queda protegida por ruleset (`lint`+`test`+`build`); el trabajo en curso no ensucia el estado publicable.

## Problemas

_(ninguno todavía)_

## Métricas

- Tests escritos: 0
- Tests pasando: 15/15 (suite de Fase 0)
- Cobertura: —

## Pendientes

- Feature 1.1 (scanner) con su test RED antes de implementar.
