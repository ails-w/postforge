# ADR-003 — RAG por proyecto y `knowledge/` como capa separada

- **Estado:** aceptado
- **Fecha:** 2026-09-26

## Contexto

El sistema tiene dos fuentes de información distintas que un prompt podría mezclar:

1. **Evidencia**: qué hay realmente en el repo a publicar (docs, ADRs, código, métricas).
2. **Política editorial**: cómo se escribe un post que funciona (formato de LinkedIn, hooks, keywords de reclutadores).

Mezclarlas produce dos problemas: la salida deja de ser reproducible (la recuperación por similitud es no determinista) y no se puede testear.

## Decisión

- **Un índice RAG por proyecto**: `postforge index <slug>` construye `~/.cache/postforge/<slug>/index.db` solo con el repo objetivo. Nada de índice global en la v1.
- **`knowledge/` separado**: política editorial curada a mano, versionada en git, seleccionada por arquetipo (no recuperada por similitud).
- El redactor recibe **solo tres cosas**: `brief.json` (evidencia citada) + slice de `knowledge/` del arquetipo + contrato de formato.

## Alternativas consideradas

| Alternativa | Por qué no |
|---|---|
| Índice global de todos los repos | Mezcla evidencia entre proyectos y sube el ruido; un post debe hablar de UN proyecto |
| `knowledge/` dentro del índice | La salida cambia sin cambiar el criterio; imposible testear la rúbrica |
| Sin brief (pasar chunks crudos al redactor) | Infla el contexto y el coste; el modelo rellena huecos con invenciones |

## Consecuencias

**Positivas:**

- Posts reproducibles y auditables: cada hecho tiene `archivo:línea`.
- Cuando LinkedIn cambie, se actualiza `knowledge/` y se re-ejecuta; el índice no se toca.
- Tests deterministas con golden files.

**Negativas / coste:**

- Hay que mantener `knowledge/` a mano (research → knowledge).
- El índice se reconstruye por proyecto; no hay respuestas cross-proyecto en la v1.

## Referencias

- `docs/architecture.md` — capas de contexto.
- `docs/research/` — fuente de las reglas de `knowledge/`.
- `docs/phase-plan.md` — Fase 1 (índice) y Fase 2 (brief).
