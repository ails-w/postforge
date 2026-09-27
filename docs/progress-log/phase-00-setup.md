# Fase 0: Setup, research y spikes — Log

> Log HISTÓRICO de la fase. Se acumula, no se borra.
> Estado actual → `docs/handoff.md` · Conceptos → `docs/learning/phase-00-setup.md` (+ transversal `uv.md`)

## Estado

**Estado**: Completada (2026-09-27) — a falta de verificar el CI en el primer push
**Última Actualización**: 2026-09-27

## Objetivos

- Dejar el repo vivo: scaffold + docs + knowledge + prompts.
- Investigar el dominio (formulario, reclutadores, psicología, visuales) con fuentes.
- Resolver los spikes: `opencode run --format json` y modelo de embeddings.

## Progreso

- [x] Lote 1: estructura y docs base + ADR-001/002/003 (2026-09-26)
- [x] Lote 2: research 4/4 docs con fuentes (2026-09-27)
- [x] Lote 3: `knowledge/` completo (reglas, rúbrica, taxonomía, arquetipos, visuals, examples) (2026-09-27)
- [x] Lote 4: código — uv, CLI, `llm.py`, tests, CI, ADR-004/005 (2026-09-27)
- [x] Lote 5: `prompts/` + learning + cierre de fase (2026-09-27)
- [ ] Verificar CI en el primer push (pendiente de crear el remoto)

## Tareas Completadas

### 2026-09-26 — Lote 1: base documental

- **Descripción**: scaffold con AGENTS.md, README, vision, phase-plan, handoff, architecture, development-plan, ADRs y plantillas de learning/progress-log.
- **Archivos**: 23 archivos · commit `720b1c9`.
- **Tests**: — (sin código todavía).

### 2026-09-27 — Lote 2: research

- **Descripción**: 4 docs de evidencia con fuentes primarias (LinkedIn Help, Sci Rep 2025, Jobscan) + límites del formulario verificados contra la UI.
- **Decisiones**: el corpus-baseline se retiró como doc; el oráculo vive en `docs/development-plan.md`.
- **Commits**: `243478d`, `a210f3b`, `41a67af`.

### 2026-09-27 — Lote 3: knowledge

- **Descripción**: contrato del formulario, reglas de encontrabilidad, anatomía del post, rúbrica, disclaimers, taxonomía (7 áreas / 42 skills), 5 arquetipos, recetas de visuals, examples (vacío a propósito).
- **Commits**: `3477b3c`, `953f3c2`, `4f3f48d`.

### 2026-09-27 — Lote 4: código y spikes

- **Descripción**: proyecto uv con Python 3.12, CLI Typer (5 comandos), adaptador `llm.py`, 15 tests, CI, guía `learning/uv.md`.
- **Spikes**: JSONL de opencode (ADR-005) y embeddings MiniLM vs potion (ADR-004).
- **Métricas**: 15 tests verdes; ruff limpio; corrida LLM completa estimada < USD 0,02.
- **Commits**: `d49fbe8`, `4e3951e`, `fc7848c`, `ff0f9b9`, `4d476a5`, `4e7215f`.

### 2026-09-27 — Lote 5: prompts y cierre

- **Descripción**: 4 prompts versionados + ruta de lectura en `docs/index.md` + learning y este log.
- **Archivos**: `prompts/*`, `docs/index.md`, `docs/learning/phase-00-setup.md`.

## Decisiones

1. **Python 3.12 + uv** — el ecosistema RAG manda; C# queda para la TUI futura (ADR-001).
2. **LLM por `opencode run`** — suscripción sin API keys; contrato JSONL + sesiones (ADR-002/005).
3. **RAG por proyecto vs `knowledge/`** — evidencia y política separadas (ADR-003).
4. **Embeddings MiniLM multilingüe** — con fusión léxica obligatoria (ADR-004).
5. **Batch + refine** — el chat refina; no produce.
6. **Ruta de lectura en `docs/index.md`** — el proyecto se explica por capas.

## Problemas

1. **`.atl/` colado en un commit** — *solución*: `.gitignore` + `git rm --cached` + amend.
2. **Python 3.14 sin wheels** (torch/chromadb/sqlite-vec) — *solución*: 3.12 gestionado por uv.
3. **ruff UP035** (`Sequence` desde `collections.abc`) — *solución*: import corregido.
4. **Hugging Face sin token** al bajar modelos — *solución*: funciona con warning; los modelos quedan cacheados.
5. **Oráculo ambiguo en el spike** (doc vs README del mismo módulo) — *solución*: medir a nivel proyecto en la calibración de Fase 2.

## Métricas

- Tests escritos: 15 (todos en verde)
- Commits de la fase: 16
- Archivos versionados: 78
- Cobertura: —

## Pendientes

- Primer push a GitHub: crear el remoto, verificar el CI, arrancar Fase 1 en `dev`.
