# Research — Evidencia de dominio

Capa **OBSERVADO**: acá vive la evidencia con fuentes que justifica las reglas de `knowledge/`. La lee el humano; el LLM no la consume directo.

## Reglas

- Cada doc lleva **Fecha** y **Estado: snapshot** en la cabecera.
- Cada afirmación relevante cita su fuente (link + fecha de consulta).
- Si una regla de `knowledge/` cambia, se actualiza acá la evidencia que la sostiene.
- Cuando una evidencia nueva contradice a `knowledge/`: se cita, se decide y se actualiza `knowledge/` (esta carpeta no se "corrige" hacia atrás, se anota).

## Documentos

| Doc | Pregunta que responde | Estado |
|---|---|---|
| `linkedin-form-contract.md` | ¿Qué campos y límites exactos exige el formulario «Añadir proyecto»? | ⏳ Lote 2 |
| `recruiter-search-ats.md` | ¿Cómo me encuentran y me filtran reclutadores y ATS? | ⏳ Lote 2 |
| `hooks-psychology.md` | ¿Cómo me leen (y por qué dejan de leer)? | ⏳ Lote 2 |
| `visuals-pipeline.md` | ¿Con qué imagen se postea un backend/script? | ⏳ Lote 2 |
| `corpus-baseline.md` | ¿El ingest aguanta mis repos reales? | ⏳ Lote 2 |

## Relación con otras capas

| Capa | Verbo | Destinatario |
|---|---|---|
| `docs/research/` | OBSERVADO | Humano |
| `knowledge/` | EXIGIDO | LLM |
| `docs/adr/` | DECIDIDO | Equipo futuro |
| `docs/learning/` | APRENDIDO | El que construye |

La regla práctica: si lo lee el modelo en cada generación → `knowledge/`; si lo leés vos para decidir o justificar → `docs/research/`.
