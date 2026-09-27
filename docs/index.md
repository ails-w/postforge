# Documentación de postforge

Mapa de navegación de la documentación del proyecto. Este es el **índice único** — los agentes IA y las personas lo usan para ubicarse.

## Docs

| Área | Documento | Contenido |
|------|-----------|-----------|
| **Estado actual** (mutable) | `docs/handoff.md` | Fase activa, próximo paso, riesgos |
| Visión | `docs/vision.md` | Alcance global, fuera-de-scope, competencias |
| Plan de fases | `docs/phase-plan.md` | Fases con scope, conceptos, criterio de salida y features |
| Aprendizaje | `docs/learning/` | Conceptos por fase (`phase-NN-name.md`) |
| Progreso (log) | `docs/progress-log/` | Historial por fase (`phase-NN-name.md`) |
| Decisiones | `docs/adr/` | ADRs (`ADR-0NN-*.md`) |
| Arquitectura | `docs/architecture.md` | Pipeline, capas RAG/knowledge, contrato con `opencode run` |
| Desarrollo | `docs/development-plan.md` | Testing, seams, fixtures, CI |
| Diagramas | `docs/diagrams/` | Diagramas del proyecto (Mermaid/ASCII) |
| Research | `docs/research/` | Evidencia de dominio con fuentes (4 docs) |

## Fuera de docs

| Documento | Contenido |
|-----------|-----------|
| `README.md` | Portafolio público (inglés) |
| `AGENTS.md` | Contexto estático para agentes IA |
| `knowledge/` | Política editorial que lee el LLM (se crea en el Lote 3) |
| `prompts/` | Prompts versionados del pipeline (se crean en el Lote 5) |
| `projects.yaml` | Registro de proyectos a publicar |

## Ruta de lectura

### Camino corto (~30 min)

| # | Documento | Qué responde |
|---|---|---|
| 1 | `README.md` | Qué es postforge |
| 2 | `docs/vision.md` | Alcance y qué queda fuera |
| 3 | `docs/architecture.md` | **El corazón**: pipeline, capas y uso |
| 4 | `docs/phase-plan.md` | Fases, features y criterios de salida |

### Camino completo (por niveles)

| Nivel | Documentos | Para qué |
|---|---|---|
| 0 | `docs/index.md` → `AGENTS.md` | Navegación y contrato de trabajo |
| 1 | `docs/phase-plan.md` → `docs/handoff.md` | Cómo se construye y dónde estamos |
| 2 | `docs/architecture.md` → `docs/adr/ADR-003-rag-per-project-vs-knowledge.md` → `docs/development-plan.md` | La máquina y sus decisiones |
| 3 | `knowledge/README.md` → `knowledge/linkedin-form.md` → `knowledge/hooks-psychology.md` | Qué escribe y por qué funciona |
| 4 | `docs/research/hooks-psychology.md` → `docs/research/recruiter-search-ats.md` | Evidencia con fuentes |
| 5 | `docs/learning/uv.md` → ADR-001/002/004/005 → `docs/research/visuals-pipeline.md` | Herramientas y técnica |

## Reglas de docs

- Idioma: Español. Nombres de carpetas/archivos en inglés.
- Formato: Markdown.
- Mantener `handoff.md` actualizado al iniciar/cerrar sesión.
- Al **cerrar** cada fase se crean o actualizan: `learning/phase-NN-name.md` (conceptos), `progress-log/phase-NN-name.md` (historial), `phase-plan.md` (estado) y `handoff.md` (estado actual).
- ADRs: una decisión = un archivo en `docs/adr/`; el ADR refleja la decisión vigente y se actualiza cuando la decisión cambia.
