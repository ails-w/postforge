# Plan de Fases — postforge

> Índice maestro del desarrollo. La fase activa tiene detalle expandido.
> Conceptos → `docs/learning/phase-NN-name.md` · Log → `docs/progress-log/phase-NN-name.md`
> Estado mutable → `docs/handoff.md`

## Reglas globales

- TDD estricto: RED → GREEN → REFACTOR (test ANTES de implementar).
- Código en inglés, docs en español; nombres de archivo/carpeta en inglés.
- Commits convencionales; un commit por feature.
- Al cerrar una fase: actualizar log + conceptos + phase-plan + handoff + commit.
- Fase 0 se commitea directo en `main`; a partir de la Fase 1 (features) el trabajo va en `dev` y se abre PR al cerrar cada fase.

## Resumen de fases

| # | Nombre | Estado | Conceptos | Log |
|---|--------|--------|-----------|-----|
| 0 | Setup + research + spikes | ✅ (CI en el 1.er push) | `phase-00-setup.md` | `phase-00-setup.md` |
| 1 | Ingesta + índice | ⏳ | `phase-01-ingest.md` | `phase-01-ingest.md` |
| 2 | Comprensión | ⏳ | `phase-02-understand.md` | `phase-02-understand.md` |
| 3 | Redacción + formulario | ⏳ | `phase-03-write.md` | `phase-03-write.md` |
| 4 | Visuales + cierre | ⏳ | `phase-04-visuals.md` | `phase-04-visuals.md` |

---

## Fase 0 — Setup + research + spikes ✅ (2026-09-27; CI pendiente del primer push)

**Objetivo:** Dejar el repo vivo (scaffold + docs), la evidencia de dominio investigada y los dos spikes técnicos resueltos: la salida JSON de `opencode run` y el modelo de embeddings.

### Scope

- Scaffold del repo con estructura de docs alineada a focusblock.
- 4 docs de research con fuentes y fecha (`docs/research/`).
- `knowledge/` inicial (contrato del formulario + taxonomía de keywords).
- Base de código: `uv`, Typer, pytest, ruff, CI en GitHub Actions.
- Spike: parsear la salida de `opencode run --format json` y elegir modelos (barato/fuerte) → ADR-004 y ADR-005.
- Spike: elegir modelo de embeddings multilingüe midiéndolo contra el corpus baseline → ADR-004.
- Cerrar: learning + progress-log de la fase.

### Fuera de scope

- Indexado real (Fase 1), comprensión y prompts de redacción (Fases 2-3), visuales (Fase 4).
- Índice de portafolio multi-repo.
- Publicación automatizada en LinkedIn.

### Conceptos de aprendizaje

- [ ] Entornos reproducibles con uv → `docs/learning/phase-00-setup.md`
- [ ] Salida estructurada de un LLM por CLI (JSON + validación) → idem
- [ ] Embeddings: qué son y cómo se eligen → idem
- [ ] CI para un CLI en Python → idem

### Criterio de salida

- [x] `uv run postforge --help` responde.
- [ ] CI (ruff + pytest) en verde (falta el primer push).
- [x] La salida de `opencode run --format json` se parsea; modelos barato/fuerte elegidos (ADR-005).
- [x] Modelo de embeddings elegido con medición (ADR-004).
- [x] Los 4 docs de research existen, con fuentes y fecha.
- [x] `knowledge/` existe y es consumible.
- [x] Learning y progress-log de Fase 0 completos; handoff apunta a Fase 1.

### Features (TDD)

#### Feature 0.1: Scaffold del paquete y CLI vacío ✅ (2026-09-27)

- [x] Test RED: `postforge --help` sale 0 y lista comandos.
- [x] `pyproject.toml` + `src/postforge/cli.py` con Typer (GREEN).
- [x] `uv run pytest` y `ruff` en verde; CI en GitHub Actions (pendiente verificar en el primer push).

#### Feature 0.2: Adaptador LLM (`opencode run`) ✅ (2026-09-27)

- [x] Test RED: `LlmClient.complete(prompt, model)` parsea `--format json` con un proceso falso.
- [x] `src/postforge/llm.py` con protocolo + implementación de subprocess (GREEN).
- Nota: spike real OK — JSONL de eventos + `sessionID` (ADR-005).

#### Feature 0.3: Spike de embeddings ✅ (2026-09-27)

- [x] Script de medición con preguntas fijas contra el corpus baseline (`scripts/spike_embeddings.py`).
- [x] Decisión documentada en ADR-004 (modelo, tamaño, idioma).

#### Feature 0.4: Research ✅ (2026-09-27)

- [x] `linkedin-form-contract.md`, `recruiter-search-ats.md`, `hooks-psychology.md`, `visuals-pipeline.md` con fuentes.

#### Feature 0.5: Knowledge inicial ✅ (2026-09-27)

- [x] `knowledge/` completo: contrato del formulario, reglas de escritura, rúbrica, taxonomía (7 áreas / 42 skills), 5 arquetipos, visuals y examples. + Concepto transversal `docs/learning/uv.md`.

---

## Fase 1 — Ingesta + índice ⏳

**Objetivo:** `postforge index <slug>` convierte un repo en un índice consultable, con chunking determinista y consultas que devuelven archivo:línea.

### Scope

- Scanner git-aware (respeta `.gitignore`, ignora binarios y artefactos generados).
- Chunker de markdown por headings y de código por símbolos, con metadata.
- Esquema SQLite (documentos, chunks, FTS5) + comandos `index` y `search`.

### Fuera de scope

- Embeddings y búsqueda vectorial (Fase 2).
- Comprensión y redacción.

### Conceptos de aprendizaje

- [ ] Chunking por estructura (por qué no cortar por caracteres) → `docs/learning/phase-01-ingest.md`
- [ ] BM25 y FTS5: búsqueda léxica → idem
- [ ] Tokenización y normalización de texto → idem

### Criterio de salida

- [ ] `uv run postforge index focusguard` crea el índice sin errores.
- [ ] `uv run postforge search "pam"` devuelve chunks con `archivo:línea`.
- [ ] Golden files del corpus baseline en verde.

### Features (TDD)

#### Feature 1.1: Scanner git-aware (con fallback sin git)

- [ ] Test RED: ignora `bin/`, `obj/`, `.venv/` y archivos binarios.
- [ ] Test RED: sin `.git`, hace walk con exclusiones explícitas.
- [ ] `src/postforge/ingest/scanner.py` (GREEN).

#### Feature 1.2: Chunker de markdown

- [ ] Test RED: un heading abre chunk nuevo; metadata con path y heading.
- [ ] Test RED: patrones estructurales (ADR, `modules/NN-*`, `learning/phase-*.md`) producen `section` y `order`.
- [ ] `src/postforge/ingest/chunker.py` (GREEN).

#### Feature 1.3: Chunker de código

- [ ] Test RED: funciones/clases como unidades; fallback por bloques.
- [ ] Extensión del chunker (GREEN).

#### Feature 1.4: Esquema SQLite + FTS5

- [ ] Test RED: insertar y consultar con `MATCH` sanitizado.
- [ ] `src/postforge/index/store.py` (GREEN).

#### Feature 1.5: CLI `index` y `search`

- [ ] Test RED: comandos Typer sobre un repo temporal.
- [ ] `src/postforge/cli.py` ampliado (GREEN).

---

## Fase 2 — Comprensión ⏳

**Objetivo:** `postforge brief <slug>` produce `brief.json` con stack, problema, métricas y evidencia citada — sin volcar el repo al LLM.

### Scope

- Aspecto-queries fijas (problema, stack, métricas, bug difícil, resultado).
- Embeddings locales + `sqlite-vec`; recuperación híbrida (FTS5 + vectores).
- Map-reduce: extract-facts por chunk → síntesis a `brief.json`.
- Validador anti-alucinación: todo hecho debe citar `archivo:línea`.

### Fuera de scope

- Redacción del post.
- Índice multigrafo o multi-repo.

### Conceptos de aprendizaje

- [ ] Embeddings y similitud coseno → `docs/learning/phase-02-understand.md`
- [ ] Léxico vs vectorial; búsqueda híbrida → idem
- [ ] Map-reduce sobre contexto → idem
- [ ] Contratos JSON y validación con Pydantic → idem

### Criterio de salida

- [ ] `brief.json` de focusguard contiene stack, problema y métricas.
- [ ] Cada hecho del brief tiene fuente; un hecho sin fuente hace fallar la validación.
- [ ] El coste por corrida queda documentado (modelo barato para el map).

### Features (TDD)

#### Feature 2.1: Embedder + sqlite-vec

- [ ] Test RED: vectores deterministas con `FakeEmbedder`; tabla creada.
- [ ] `src/postforge/index/embedder.py` (GREEN).

#### Feature 2.2: Recuperación híbrida

- [ ] Test RED: la fusión prioriza chunks relevantes en el corpus baseline.
- [ ] `src/postforge/index/retriever.py` (GREEN).

#### Feature 2.3: Extract-facts (map) + synthesize-brief (reduce)

- [ ] Test RED: con `FakeLlm` canónico, el brief resultante valida contra el schema.
- [ ] `src/postforge/understand/` (GREEN).

#### Feature 2.4: Validador de citas

- [ ] Test RED: hecho sin `source` → error con detalle.
- [ ] `src/postforge/understand/validator.py` (GREEN).

#### Feature 2.5: CLI `brief`

- [ ] Test RED: `postforge brief focusguard` escribe `out/<slug>/brief.json`.
- [ ] `src/postforge/cli.py` ampliado (GREEN).

---

## Fase 3 — Redacción + formulario ⏳

**Objetivo:** `postforge gen <slug>` produce `post.md`, `form.md` y `checklist.md` listos para pegar, dentro de los límites del formulario y aprobando la rúbrica.

### Scope

- Selector de arquetipo (backend-api, cli-systems, data-rag, docs-learning, iac-security).
- Plantillas Jinja2 + prompts `write-post` y `critique-post` con rúbrica.
- `refine`: sesión de chat sobre la variante elegida (reusa el `sessionID` de opencode).
- `form.md`: nombre ≤ 255, descripción ≤ 2000, 5 aptitudes con evidencia, fechas, colaboradores.
- `checklist.md`: pasos previos a publicar.

### Fuera de scope

- Visuales (Fase 4).
- Publicación (siempre manual).

### Conceptos de aprendizaje

- [ ] Prompt versionado y separación prompt/código → `docs/learning/phase-03-write.md`
- [ ] Plantillas y contratos de formato → idem
- [ ] Evaluación de salida con rúbrica → idem

### Criterio de salida

- [ ] `postforge gen focusguard` genera los 3 artefactos.
- [ ] Las longitudes respetan 255/2000; las 5 aptitudes salen de la taxonomía con evidencia.
- [ ] La rúbrica se cumple (o el critique explica qué falló).

### Features (TDD)

#### Feature 3.1: Selector de arquetipo

- [ ] Test RED: focusguard → iac-security; focusblock → cli-systems.
- [ ] `src/postforge/write/archetype.py` (GREEN).

#### Feature 3.2: Plantilla de post + variantes

- [ ] Test RED: render determinista con brief canónico.
- [ ] `src/postforge/write/render.py` + `knowledge/templates/` (GREEN).

#### Feature 3.3: Critique con rúbrica

- [ ] Test RED: post con hook débil no aprueba.
- [ ] `src/postforge/write/critique.py` (GREEN).

#### Feature 3.4: `form.md` + `checklist.md`

- [ ] Test RED: descripción de 2001 chars → falla con mensaje claro.
- [ ] `src/postforge/write/form.py` (GREEN).

#### Feature 3.5: CLI `gen`

- [ ] Test RED: `postforge gen` escribe `out/<slug>/<fecha>/`.
- [ ] `src/postforge/cli.py` ampliado (GREEN).

#### Feature 3.6: `refine` (chat)

- [ ] Test RED: el refine reusa el `sessionID` y persiste la versión final.
- [ ] `src/postforge/write/refine.py` + CLI (GREEN).

---

## Fase 4 — Visuales + cierre ⏳

**Objetivo:** `postforge visuals <slug>` genera la media del post y el README muestra el flujo end-to-end.

### Scope

- Diagramas Mermaid del repo → PNG con tema consistente (`mmdc`).
- Snippet de código (silicon) y GIF de terminal (vhs).
- Portada del post (plantilla HTML → PNG).
- README con demo end-to-end.

### Fuera de scope

- Edición manual de imágenes.
- Publicación (siempre manual).

### Conceptos de aprendizaje

- [ ] Diagramas como código y renderizado → `docs/learning/phase-04-visuals.md`
- [ ] Media para redes: tamaños y formatos → idem
- [ ] Grabación de terminal reproducible → idem

### Criterio de salida

- [ ] `postforge visuals focusguard` genera ≥ 1 PNG de diagrama y ≥ 1 GIF de terminal.
- [ ] Los diagramas usan un tema consistente.
- [ ] README con demo end-to-end y captura.

### Features (TDD)

#### Feature 4.1: Mermaid → PNG

- [ ] Test RED: markdown con bloque mermaid → PNG esperado.
- [ ] `src/postforge/visuals/mermaid.py` (GREEN).

#### Feature 4.2: GIF de terminal

- [ ] Test RED: guion vhs generado desde un comando de demo.
- [ ] `src/postforge/visuals/terminal.py` (GREEN).

#### Feature 4.3: Snippet y portada

- [ ] Test RED: portada con título + stack; snippet con resaltado.
- [ ] `src/postforge/visuals/` (GREEN).

#### Feature 4.4: Demo en README

- [ ] README con el flujo completo y media generada.
