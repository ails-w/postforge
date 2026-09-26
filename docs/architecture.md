# Arquitectura — postforge

> Estructura objetivo y flujo de datos. El árbol mezcla lo implementado con lo planificado; la fase activa manda (`docs/handoff.md`).

## El dato que lo explica todo

**Evidencia y política son capas separadas.** El RAG sabe *qué hay* en el repo; `knowledge/` sabe *cómo se escribe* un post. El LLM no decide el flujo: Python orquesta lo determinista y llama al modelo solo donde aporta (extraer, sintetizar, redactar).

| Capa | Pregunta | Origen | Consumo |
|---|---|---|---|
| RAG (índice del proyecto) | ¿Qué hay en ESTE repo? | Autogenerado por `ingest`/`index` | Recuperación por similitud |
| `knowledge/` | ¿Cómo se escribe un post que funciona? | Curado a mano | Selección por arquetipo |
| `prompts/` | ¿Qué le pedimos exactamente al modelo? | Curado a mano | Las 3 llamadas al LLM |
| Contrato de formato | ¿Qué campos y límites exige LinkedIn? | `knowledge/linkedin-form.md` | Validación de salida |

Si estas capas se mezclan, la salida deja de ser reproducible y no se puede testear. Ver `docs/adr/ADR-003-rag-per-project-vs-knowledge.md`.

## Pipeline

```text
repo (ruta)
   │
   ▼
┌────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│   ingest   │───▶│    index     │───▶│    understand    │───▶│    write     │
│ scan+chunk │    │ FTS5 + vec   │    │  map-reduce LLM  │    │ plantillas + │
└────────────┘    └──────────────┘    └──────────────────┘    │   critique   │
                        ▲                     brief.json       └──────────────┘
                        │                                          │
                 projects.yaml                                     ▼
                                                         out/<slug>/<fecha>/
                                                         ├── brief.json
                                                         ├── post.md
                                                         ├── form.md
                                                         └── checklist.md

docs/ del repo ──▶ visuals (mmdc / vhs / silicon) ──▶ media/*.png|gif ──▶ out/.../media/
```

## Componentes

| Módulo | Responsabilidad | Entrada → Salida |
|---|---|---|
| `ingest/scanner.py` | Enumerar archivos respetando `.gitignore` | ruta → lista de paths |
| `ingest/chunker.py` | Partir markdown por headings y código por símbolos | path → chunks con metadata |
| `index/store.py` | Persistir documentos, chunks y FTS5 | chunks → `index.db` |
| `index/embedder.py` | Embeber chunks con fastembed (ONNX) | texto → vectores |
| `index/retriever.py` | Fusión híbrida (BM25 + coseno) | query → top-k chunks |
| `understand/extract.py` | Map: hechos por chunk con citas | chunks → facts |
| `understand/brief.py` | Reduce: hechos → brief validado | facts → `brief.json` |
| `understand/validator.py` | Todo hecho cita `archivo:línea` | brief → válido/error |
| `write/archetype.py` | Elegir arquetipo por stack detectado | brief → arquetipo |
| `write/render.py` | Jinja2: post y variantes | brief + arquetipo → `post.md` |
| `write/form.py` | Campos del formulario con límites | brief → `form.md` |
| `write/critique.py` | Rúbrica: hook, keywords, especificidad | post → score + razones |
| `visuals/*` | Diagramas, GIF, snippet, portada | repo → `media/` |
| `llm.py` | Adaptador `opencode run` | prompt+modelo → JSON |

## Contrato con el LLM

El LLM se invoca **siempre** por el adaptador `llm.py`, que ejecuta:

```text
opencode run -m <provider/model> --format json "<prompt>"
```

Tres llamadas por corrida, nunca más:

1. `extract-facts` — modelo barato, un chunk por llamada (map).
2. `synthesize-brief` — modelo barato, reduce sobre los hechos.
3. `write+critique` — modelo fuerte, una vez por variante.

Reglas:

- El prompt vive en `prompts/` y se versiona; `llm.py` no contiene texto de negocio.
- La salida se valida con Pydantic antes de tocar disco; si no valida, se reintenta una vez y se aborta con el error crudo.
- En CI nunca se llama: se usa `FakeLlm` (ver `docs/development-plan.md`).

## Datos y caché

| Dato | Ubicación | Versionado |
|---|---|---|
| Registro de proyectos | `projects.yaml` | Sí (git) |
| Índice RAG por proyecto | `~/.cache/postforge/<slug>/index.db` | No (se reconstruye) |
| Salidas del pipeline | `out/<slug>/<fecha>/` | No (local, gitignored) |
| Knowledge y prompts | `knowledge/`, `prompts/` | Sí (git) |

## Estructura del repo

```text
postforge/
├── AGENTS.md · README.md · projects.yaml
├── pyproject.toml · .python-version · uv.lock
├── src/postforge/
│   ├── cli.py · config.py · llm.py · models.py
│   ├── ingest/ · index/ · understand/ · write/ · visuals/ · output/
├── tests/ (+ fixtures/)
├── prompts/
├── knowledge/
└── docs/
    ├── index.md · vision.md · phase-plan.md · handoff.md
    ├── architecture.md · development-plan.md
    ├── adr/ · learning/ · progress-log/ · diagrams/ · research/
```

## Decisiones relacionadas

- `docs/adr/ADR-001-python-uv-stack.md` — lenguaje y entorno.
- `docs/adr/ADR-002-opencode-run-llm-backend.md` — cómo se invoca el LLM.
- `docs/adr/ADR-003-rag-per-project-vs-knowledge.md` — separación de capas.
