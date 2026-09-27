# Ganchos y psicología del texto

- **Fecha:** 2026-09-27
- **Estado:** snapshot
- **Pregunta:** ¿cómo me leen (y por qué dejan de leer)?

## Restricciones duras (verificadas)

| Restricción | Valor | Fuente |
|---|---|---|
| Largo máximo de un post | 3.000 caracteres (si te pasás, LinkedIn sugiere un artículo) | LinkedIn Help `a528176` |
| Truncado «ver más» en el feed | ~210 caracteres en desktop · ~140 en móvil | Guías de industria 2026, coincidentes |
| El hook tiene que vivir antes del corte | ≤ 140 caracteres con cifra o contraste | Derivado de lo anterior |

## La psicología (con la evidencia y su matiz)

### Information gap / curiosity gap

- **Teoría:** la curiosidad aparece ante un hueco de información y la relación entre confianza y curiosidad es **curvilínea** (máxima cuando la confianza es media, ~0,45-0,55 en una escala 0-1).
- **Evidencia de campo:** Aubin Le Quéré & Matias, *Scientific Reports* 2025 ([PMC11704130](https://pmc.ncbi.nlm.nih.gov/articles/PMC11704130/)), meta-analizaron **8.977 experimentos** de titulares (Upworthy) y encontraron que la concreción:
  - **ayuda** cuando el titular base es vago;
  - **perjudica** cuando el titular ya es muy concreto;
  - el óptimo es «middling»: ni vago ni sobre-especificado.
- **Regla postforge:** curiosidad **con** concreción — el hook promete algo específico y deja abierto el cómo/por qué. Ni «Descubrí algo increíble» (vago) ni «Reescribí 47 archivos, 312 líneas, 6 módulos y 14 tests» (muro).

### Otras palancas (práctica de industria)

- **Pattern interrupt:** romper el scroll requiere algo inesperado (un número, un error confesado).
- **Social proof:** resultados y números verificables.
- **Loss aversion:** el costo de un error se recuerda más que un logro abstracto.
- **Especificidad concreta:** sustantivos y cifras en lugar de adjetivos.

Estas cuatro son práctica profesional documentada; no hay un estudio único que las respalde con la fuerza del anterior, así que en `knowledge/rubric.md` pesan menos que la evidencia dura.

## Estructura de post que implementa postforge

1. **Hook** (≤ 140 caracteres): cifra o contraste, con curiosidad concreta.
2. **Problema** (2-3 líneas): el dolor real.
3. **Qué hice** (bullets): stack nombrado, decisiones concretas.
4. **Prueba**: métrica, test o resultado verificable del repo.
5. **CTA**: pregunta o invitación humilde.
6. **3-5 hashtags** de nicho.

Formato: párrafos de 1-2 líneas; el corte del feed nunca debe partir una frase.

## Anti-patrones

| Anti-patrón | Por qué falla |
|---|---|
| Hype vacío («Estoy emocionado de compartir…») | No hay hueco de información: nada que resolver |
| Clickbait vago | Evidencia: la concreción baja tiene peor desempeño que la media |
| Sobre-especificar el hook | Evidencia: la concreción excesiva baja el CTR |
| Muro de texto | Nadie cruza el corte hacia arriba |
| Hashtags genéricos (#motivation, #ai) | No segmentan a nadie |

## Cómo se aplica en postforge

- `knowledge/rubric.md` puntúa: hook ≤ 140 con concreción, métrica citada, cobertura de keywords, longitud, ausencia de hype.
- `prompts/write-post.md` implementa las fórmulas de hook.
- El pipeline genera 2-3 variantes con fórmulas distintas y `critique` elige o penaliza.

## Fórmulas de hook (candidatas)

| Fórmula | Plantilla | Riesgo del que cuida |
|---|---|---|
| Métrica | «Reduje X de A a B» | Vago → concreto |
| Contraste | «Todos hacen X. Yo hice Y.» | Pattern interrupt |
| Error confesado | «X me costó N horas; la causa era Y» | Loss aversion |
| Pregunta específica | «¿Por qué X falla cuando Y?» | Curiosity gap |
| Resultado inesperado | «Esperaba X; encontré Y» | Pattern interrupt |

## Fuentes

| Fuente | Uso | Consultado |
|---|---|---|
| [LinkedIn Help a528176](https://www.linkedin.com/help/linkedin/answer/a528176) | límite de 3.000 caracteres | 2026-09-27 |
| [Sci Rep 2025 — When curiosity gaps backfire](https://pmc.ncbi.nlm.nih.gov/articles/PMC11704130/) | relación curvilínea concreción/CTR en 8.977 experimentos | 2026-09-27 |
| Guías de truncado 2026 (authoredup, taplio, flypost) | ~210 desktop / ~140 móvil | 2026-09-27 |
| Práctica de copywriting (robpalmer, copyhackers) | palancas y anti-patrones | 2026-09-27 |
