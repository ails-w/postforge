# Fase 1: Ingesta + índice — Log

> Log HISTÓRICO de la fase. Se acumula, no se borra.
> Estado actual → `docs/handoff.md` · Conceptos → `docs/learning/phase-01-ingest.md`

## Estado

**Estado**: En Progreso
**Última Actualización**: 2026-10-05 19:10

## Objetivos

- `postforge index <slug>` convierte un repo en un índice consultable.
- Chunking determinista con metadata (`archivo:línea`).
- `postforge search "<query>"` devuelve chunks con `archivo:línea`.
- Golden files del corpus baseline (`focusguard`, `focusblock`) en verde.

## Progreso

- [x] Feature 1.1: Scanner git-aware (con fallback sin git) (2026-10-05)
- [ ] Feature 1.2: Chunker de markdown
- [ ] Feature 1.3: Chunker de código
- [ ] Feature 1.4: Esquema SQLite + FTS5
- [ ] Feature 1.5: CLI `index` y `search`

## Tareas Completadas

### 2026-10-05 — Feature 1.1: Scanner git-aware

- **Descripción**: `scan_repo(root)` enumera los archivos del proyecto. Con git usa `git ls-files` (solo trackeados); sin git hace walk con exclusiones explícitas. Descarta binarios (byte NUL) y devuelve rutas relativas ordenadas.
- **Archivos**: `src/postforge/ingest/__init__.py`, `src/postforge/ingest/scanner.py`, `tests/test_scanner.py`.
- **Tests**: 4 nuevos (19 en total, todos verdes).
- **Decisión**: `list_tracked_files` usa `git ls-files` (solo trackeados), no `--others`; el proyecto publica repos terminados y se prioriza reproducibilidad.

### 2026-10-05 — Kickoff de la fase

- **Descripción**: Apertura de Fase 1 en rama `dev` (regla del phase-plan). Documento de conceptos y log creados desde plantilla. Ramas y CI ya preparados.
- **Archivos**: `docs/learning/phase-01-ingest.md`, `docs/progress-log/phase-01-ingest.md`.
- **Tests**: — (sin código todavía).

## Decisiones

1. **Fase 1 trabaja en `dev`** — *por qué*: `main` queda protegida por ruleset (`lint`+`test`+`build`); el trabajo en curso no ensucia el estado publicable.

## Problemas

_(ninguno todavía)_

## Métricas

- Tests escritos: 4 (Fase 1) · 19 en total
- Tests pasando: 19/19 (100%)
- Cobertura: —

## Pendientes

- Feature 1.2: chunker de markdown (test RED primero).
