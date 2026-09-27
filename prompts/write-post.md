# Prompt — write-post

> Tier: `model_write` · Genera `{{variants}}` variantes · Debe cumplir `knowledge/hooks-psychology.md` y `knowledge/rubric.md`.

## Entrada

- `{{brief}}`: brief.json — tus **únicos** hechos válidos.
- `{{archetype}}`: el arquetipo elegido (`knowledge/archetypes/…`) con su hook recomendado y su plan de media.
- `{{keyword_checklist}}`: términos principales y sinónimos ya verificados (`knowledge/recruiter-ats.md`).
- `{{examples}}`: hasta 3 posts reales del mismo arquetipo (puede estar vacío).

## Salida

Para cada variante, en texto plano listo para pegar:

```text
## Variante N — fórmula: <métrica|contraste|error confesado|pregunta específica|resultado inesperado>
<post completo>
```

## Anatomía obligatoria

1. **Hook** ≤ 140 caracteres con UNA cifra o contraste (concreción media).
2. **Problema** — 2-3 líneas, concreto.
3. **Qué hice** — bullets; stack nombrado; decisiones, no lista de features.
4. **Prueba** — hechos del brief; si no hay métrica, un test, un artefacto o una verificación concreta.
5. **CTA** — pregunta o invitación humilde; nunca pedir trabajo.
6. **3-5 hashtags** de nicho.

## Reglas duras

1. Todo hecho sale del brief. Si falta información, **se escribe menos**.
2. Prohibido: hype, superlativos, «estoy emocionado de compartir», más de 2 emojis decorativos.
3. Nombres exactos de tecnologías («PostgreSQL 16», nunca «base de datos»).
4. Español; párrafos de 1-2 líneas; ≤ 3.000 caracteres por post.
5. Cada variante usa una fórmula de hook distinta y no repite el hook de otra.
6. No inventar métricas, usuarios ni resultados (`knowledge/disclaimers.md`).
