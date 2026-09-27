# knowledge/ — Política editorial (lo que el LLM lee)

Esta carpeta es la capa **EXIGIDO**: reglas operativas que el pipeline inyecta en los prompts. No es evidencia (eso vive en `docs/research/`) ni decisiones (`docs/adr/`) ni conceptos aprendidos (`docs/learning/`).

## Regla de pertenencia

> Si un documento lo lee el **modelo** en cada generación → `knowledge/`.
> Si lo lee el **humano** para decidir o justificar → `docs/research/`.

Cada regla de acá tiene su fuente en `docs/research/` o en un ADR. Si la evidencia cambia, se actualiza acá.

## Archivos y consumidor

| Archivo | Qué contiene | Lo consume |
|---|---|---|
| `linkedin-form.md` | Contrato operativo del formulario: campos, límites, validaciones | `write/form.py` |
| `recruiter-ats.md` | Reglas de encontrabilidad: nombrar stack, keywords, aptitudes | `write/*` |
| `hooks-psychology.md` | Anatomía del post, fórmulas de hook, anti-patrones | `prompts/write-post.md`, `write/critique.py` |
| `rubric.md` | Criterios de evaluación y pesos | `write/critique.py` |
| `disclaimers.md` | Qué NO afirmar nunca | Todos los prompts |
| `keyword-taxonomy.yaml` | Vocabulario del dominio: área → skill → sinónimos ES/EN | `write/form.py`, retrieval |
| `archetypes/` | Plan por tipo de proyecto (media, métrica, tono) | `write/archetype.py` |
| `visuals.md` | Recetas de media y specs | `visuals/*` |
| `examples/` | Posts de referencia (few-shot) | `prompts/write-post.md` |

## Reglas de escritura de esta carpeta

- Reglas cortas y accionables; esto se inyecta al prompt, no es un ensayo.
- Cada archivo declara su fuente (`Fuente: docs/research/<doc>.md`).
- Sin duplicar: si aplica a todos los arquetipos, va acá; si es de uno, va en su arquetipo.
