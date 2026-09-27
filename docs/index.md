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

## Reglas de docs

- Idioma: Español. Nombres de carpetas/archivos en inglés.
- Formato: Markdown.
- Mantener `handoff.md` actualizado al iniciar/cerrar sesión.
- Al **cerrar** cada fase se crean o actualizan: `learning/phase-NN-name.md` (conceptos), `progress-log/phase-NN-name.md` (historial), `phase-plan.md` (estado) y `handoff.md` (estado actual).
- ADRs: una decisión = un archivo en `docs/adr/`; el ADR refleja la decisión vigente y se actualiza cuando la decisión cambia.
