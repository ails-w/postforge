# AGENTS.md — postforge

> Contexto ESTÁTICO del proyecto. Persona, tono y protocolos de memoria viven en el AGENTS.md global (`~/.config/opencode/AGENTS.md`); este archivo NO los repite.
> Lo mutable (fase activa, próximo paso, riesgos) vive SOLO en `docs/handoff.md`.

## Overview

postforge es un CLI en Python que genera posts de LinkedIn y los campos del formulario "Añadir proyecto" a partir de la documentación real de un repositorio local. Corre un RAG por proyecto: ingesta → índice (SQLite FTS5 + embeddings) → comprensión (`brief.json`) → redacción. El LLM es un modelo de la suscripción de OpenCode, invocado por terminal con `opencode run`.

El dato arquitectónico que lo explica todo: **evidencia y política son capas separadas**. El RAG (índice del repo objetivo) aporta los hechos; `knowledge/` aporta el criterio editorial; y el LLM no orquesta nada: Python hace lo determinista y lo llama en 3 puntos (extraer hechos, sintetizar brief, redactar y criticar).

## Stack (fijado)

| Capa | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.12 (gestionado con uv) |
| CLI | Typer + Rich | — |
| Índice | SQLite FTS5 + sqlite-vec | — |
| Embeddings | fastembed (ONNX, multilingüe) | — |
| Plantillas | Jinja2 | — |
| Datos | Pydantic v2 + PyYAML | — |
| LLM | `opencode run --format json` (suscripción OpenCode) | opencode v2 |
| Testing | pytest + ruff | — |
| Visuales | mmdc (mermaid-cli), vhs, silicon, matplotlib | — |

## Comandos

- Instalar entorno: `uv sync`
- Ejecutar: `uv run postforge --help`
- Tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Formato: `uv run ruff format .`
- Modelos disponibles: `opencode models`
- **NUNCA ejecutar**: publicación automatizada en LinkedIn — no existe API para el perfil personal y automatizar el login arriesga la cuenta (ver `docs/adr/ADR-002-opencode-run-llm-backend.md`).

## Mapa del repo

Estructura objetivo y pipeline → `docs/architecture.md`. El árbol mezcla lo implementado con lo planificado; la fase activa manda.

## Convenciones

- **Código en inglés, docs en español; nombres de carpeta y archivo en inglés** — *Reason:* el código es artefacto técnico; los docs son para el estudiante.
- **Python**: `snake_case`, type hints obligatorios, líneas ≤ 100 chars, formato con ruff — *Reason:* estándar del ecosistema.
- **Conventional commits**: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:` — *Reason:* historial legible y verificable.
- **Sin "Co-Authored-By" ni atribución IA** — *Reason:* regla global del usuario.
- **Docs: bloques de código con cabecera `python`** (nunca `py`) — *Reason:* convención del usuario.
- **No duplicar contenido entre archivos**: si hay que copiar un párrafo, está mal ubicado.

## TDD ESTRICTO (regla dura)

- NUNCA escribir implementación sin test previo. Ciclo: RED → GREEN → REFACTOR.
- Nombre de tests: `test_<unidad>_<condición>_<resultado_esperado>`.
- Si el usuario pide código sin test, primero escribir el test RED y luego el código mínimo para GREEN.
- Los tests son parte de la definición de "terminado" (DoD).

## Rol de aprendizaje (objetivo principal)

Este es un proyecto de **APRENDIZAJE**. El objetivo es que el estudiante entienda, no solo que el código funcione.

- Explicá el **PORQUÉ técnico**: concepto → problema que resuelve → cómo se aplica acá.
- **Proponé alternativas** con trade-offs; no te limites a ejecutar.
- Tono pedagógico en cada explicación.
- **EXCEPCIÓN al contrato de respuestas cortas del global**: en modo enseñanza, expandí.

## Testing

- pytest + ruff. Dobles obligatorios para el LLM y los embeddings (ver `docs/development-plan.md`).
- Los tests de CI **nunca** llaman a `opencode run` ni descargan modelos.
- Corpus de referencia: los 3 repos de `docs/research/corpus-baseline.md` como golden files.

## Límites / Do-nots

- NO inventar métricas, stacks ni resultados que no estén en el repo fuente (`knowledge/disclaimers.md`).
- NO mezclar `knowledge/` dentro del índice RAG: son capas distintas (`docs/adr/ADR-003-rag-per-project-vs-knowledge.md`).
- NO crear carpetas vacías ni duplicar contenido.
- NO modificar `docs/handoff.md` salvo al iniciar/cerrar sesión.
- NO automatizar login ni publicación en LinkedIn.

## Gotchas conocidos

- **Python 3.14 del sistema sin wheels** — *Reason:* torch/chromadb/sqlite-vec fallan al instalar; usar 3.12 con `uv python install 3.12`.
- **FTS5 interpreta operadores en `MATCH`** — *Reason:* términos con caracteres especiales rompen la query; sanitizar antes de buscar.
- **`opencode run` usa el servicio en segundo plano** — *Reason:* para aislar un problema usar `--standalone`; la salida JSON se pide con `--format json`.

## Git + Definition of Done

- Ramas: `main` + `dev`. En Fase 0 se commitea directo en `main`; al iniciar la primera fase de features, el trabajo va en `dev` y se abre PR al cerrar cada fase.
- Un commit por feature; conventional commits en inglés.
- DoD de una feature: test RED que pasa (GREEN) + refactor + commit convencional.
- El aprendizaje se documenta al cerrar la fase en `docs/learning/phase-NN-name.md`, junto con `progress-log/`, `phase-plan.md` y `handoff.md`.

## Tabla de punteros

| Área | Documento |
|---|---|
| **Estado actual** (LEER al iniciar, ACTUALIZAR al cerrar) | `docs/handoff.md` |
| Mapa de navegación completo | `docs/index.md` |
| Plan de fases (scope + criterios de salida) | `docs/phase-plan.md` |
| Arquitectura y pipeline | `docs/architecture.md` |
| Estrategia de testing y seams | `docs/development-plan.md` |
