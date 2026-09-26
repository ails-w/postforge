# Visión del Proyecto — postforge

postforge convierte la documentación real de un repositorio en un post de LinkedIn listo para pegar, y en los campos del formulario «Añadir proyecto». Existe para automatizar un proceso que hoy es lento: contar bien lo que se construyó, con evidencia y sin inflar.

## Resultado buscado

Al finalizar el proyecto, debe servir como evidencia práctica de dominio en:

- Diseño de un pipeline RAG local (ingesta, chunking, índice híbrido, recuperación).
- Comprensión y compresión de contexto para LLMs (map-reduce, briefs con evidencia citada).
- Prompt engineering versionado y evaluación de salida (rúbrica).
- Integración de un LLM por CLI contra una suscripción (sin API keys) con salida estructurada.
- Testing determinista de un sistema no determinista (seams, fakes, golden files).

## Alcance funcional

| Módulo | Propósito de negocio | Propósito de aprendizaje |
|---|---|---|
| `ingest` | Escanear un repo y extraer evidencia útil | Chunking por estructura (headings/símbolos) |
| `index` | Índice híbrido por proyecto | FTS5/BM25 + embeddings locales |
| `understand` | Comprimir evidencia a `brief.json` | Map-reduce, citas, anti-alucinación |
| `write` | Redactar post y campos del formulario | Prompts versionados, plantillas, rúbrica |
| `visuals` | Generar media para el post | Diagramas como código, capturas, portada |

## Fuera de alcance inicial

- Publicación automática en LinkedIn (no hay API para el perfil personal; automatizar el login arriesga la cuenta).
- Índice global de portafolio (la v1 indexa un proyecto por corrida).
- TUI: la v1 es CLI. **Upgrade path:** una TUI en C#/.NET consume los mismos artefactos (`brief.json`, `post.md`, `form.md`) sin tocar el core (patrón daemon/TUI de focusblock).
- Traducción automática del post: se escribe en el idioma configurado por proyecto.

## Competencias técnicas

### Python / CLI

- Gestión de entorno reproducible con uv, packaging, Typer/Rich.

### RAG / Datos

- Chunking por estructura, SQLite FTS5, embeddings ONNX, búsqueda híbrida.

### LLM / Prompts

- Contratos de salida JSON, map-reduce, rúbricas de evaluación.

### Calidad

- TDD estricto, seams, fakes, golden files, ruff.

## Principio de aprendizaje

La prioridad siempre es **entender el concepto antes de escribir la solución**. Cada fase declara sus conceptos de aprendizaje en `docs/phase-plan.md` y se documentan al cerrarse en `docs/learning/`. TDD estricto: test primero, implementación después.
