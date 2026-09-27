# prompts/ — Prompts versionados del pipeline

Los prompts son **código**: se revisan en git, se testean con `FakeLlm` y no viven dentro de `src/`.

| Prompt | Cuándo corre | Tier | Salida |
|---|---|---|---|
| `extract-facts.md` | Una vez por chunk (map) | modelo barato | JSON de hechos con cita |
| `synthesize-brief.md` | Una vez por corrida (reduce) | modelo barato | `brief.json` |
| `write-post.md` | Una vez por corrida | modelo fuerte | 2-3 variantes |
| `critique-post.md` | Una vez por variante | modelo fuerte | JSON de rúbrica |

## Composición de una llamada

```text
prompt del archivo  +  slice de knowledge/ del arquetipo  +  brief.json  +  contrato de formato
```

Al modelo nunca se le pasa el repo crudo: para eso están el RAG (Fases 1-2) y el brief.

## Reglas

- Placeholders en `{{llaves}}`; el código los sustituye con Jinja2.
- Un cambio de prompt = un commit convencional (`docs(prompts): ...`); si altera la salida, se corre `critique` de regresión con el brief canónico.
- Este directorio no contiene datos personales ni secretos (ver `docs/architecture.md` §Datos que NUNCA entran al repo).
