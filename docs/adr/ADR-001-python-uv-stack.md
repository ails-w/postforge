# ADR-001 — Python 3.12 + uv como stack de la v1

- **Estado:** aceptado
- **Fecha:** 2026-09-26

## Contexto

postforge es un CLI que corre un pipeline RAG local (chunking, índice, embeddings) y llama a un LLM por terminal. El autor viene de proyectos en C#/.NET (focusblock) y quiere el camino más corto a algo funcionando, sin renunciar a calidad de testing.

## Decisión

La v1 se implementa en **Python 3.12 gestionado con uv**. C#/.NET 10 queda como **upgrade path** para una TUI futura, que consumirá los artefactos (`brief.json`, `post.md`, `form.md`) sin tocar el core.

## Alternativas consideradas

| Alternativa | Por qué no |
|---|---|
| C#/.NET 10 completo | El ecosistema RAG/embeddings es más maduro y con menos fricción en Python; duplicaría esfuerzo para un CLI que ya se resuelve |
| Híbrido C# (CLI) + Python (RAG) | Dos runtimes, dos toolchains y un contrato IPC para un MVP "corto y eficiente" |
| Python del sistema (3.14) | Sin wheels para torch/sqlite-vec; se fija 3.12 con uv |

## Consecuencias

**Positivas:**

- `uv` da entorno reproducible y rápido (`uv sync`, `uv run`).
- El CLI y el RAG viven en un solo lenguaje; el contrato con el LLM es un subprocess.
- La separación por artefactos deja la puerta abierta a la TUI C#.

**Negativas / coste:**

- Se pierde el "modo enseñanza" de C# fuera de este proyecto.
- Hay que mantener discipline en tipado (type hints + ruff) para compensar la falta de compilador estricto.

## Referencias

- `docs/architecture.md` — contrato de artefactos para la futura TUI.
- `docs/handoff.md` — riesgos de entorno (Python 3.14).
