# Aprendizaje por Fase

Cada fase documenta los CONCEPTOS aprendidos en **UN archivo** `phase-NN-name.md` (no el log de tareas — eso vive en `docs/progress-log/`).

## Archivos

| Fase | Archivo | Estado |
|------|---------|--------|
| 0 | `phase-00-setup.md` | ⏳ |
| 1 | `phase-01-ingest.md` | ⏳ |
| 2 | `phase-02-understand.md` | ⏳ |
| 3 | `phase-03-write.md` | ⏳ |
| 4 | `phase-04-visuals.md` | ⏳ |

## Plantilla

Usar `template-phase.md` para cada fase nueva. Cada archivo abre con un **glosario** y un **mapa de conceptos**, y cada concepto se desarrolla con una **capa de fundamentos**:

- **En una frase** — la idea central, sin jerga.
- **Fundamentos previos** — los términos e ideas que hay que entender ANTES. Se explican en el momento, sin asumir conocimiento previo.
- **Qué es** / **Qué problema resuelve** / **Cómo funciona paso a paso**.
- **Qué se rompería sin esto en postforge** — contrafactual concreto del proyecto.
- **Para qué sirve en este proyecto** / **Cómo se usa (código real)**.
- **Error común** / **Para profundizar**.

## Contenido por Archivo

- `phase-NN-name.md` — conceptos de la fase con glosario, mapa de conceptos y capa de fundamentos. No asume que el lector ya conoce las primitivas.

## Reglas

- Se acumula: los conceptos aprendidos NUNCA se borran.
- Se escribe **al cerrar la fase**, a partir de lo aprendido durante ella.
- Cada concepto debe tener su "Error común" — es lo que demuestra comprensión real.
