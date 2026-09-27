# Contrato operativo — Formulario «Añadir proyecto»

Fuente: `docs/research/linkedin-form-contract.md` + capturas de la UI (2026-09-26).

## Salida requerida (`form.md`)

| # | Bloque | Regla dura | Validación |
|---|---|---|---|
| 1 | Nombre del proyecto | ≤ 255 caracteres; nombre real del producto | `len <= 255` |
| 2 | Descripción | ≤ 2.000 caracteres; apuntar a 350-500 palabras | `len <= 2000` |
| 3 | Aptitudes | exactamente 5, de la taxonomía, con evidencia en el repo | `len == 5`, cada una con cita |
| 4 | Fechas | inicio y fin mes/año; fin `null` → «trabajando actualmente» | contra `projects.yaml` |
| 5 | Colaboradores | solo los registrados en `projects.yaml` | — |
| 6 | Asociado con | del `projects.yaml` | — |
| 7 | Media | 1-3 piezas con ruta y medidas | `len <= 50` (límite LinkedIn) |

## Reglas de redacción de la descripción

1. Primera línea = el resultado principal (no «Este proyecto es…»). El perfil también recorta la descripción.
2. Estructura: problema → qué hace → stack nombrado → resultado o prueba.
3. Nombres exactos de tecnologías (regla de `recruiter-ats.md`).
4. Sin hype (anti-patrones de `hooks-psychology.md`).
5. Español por defecto. Para otro idioma se agrega `language` por proyecto en `projects.yaml` (Fase 3).

## Prohibido

- Métricas que no estén en `brief.json` con cita.
- Mencionar colaboradores que no aportaron (LinkedIn les notifica).
- Pegar el post del feed tal cual: **son artefactos distintos** (`post.md` cuenta, `form.md` registra).

## Media: cuántas piezas y cómo se usan

- **Recomendado: 2** (una principal + una de prueba). Máximo 3 en proyectos insignia. El formulario admite 50, la atención no.
- Se generan en `out/<slug>/<fecha>/media/` (local, gitignored) y se suben **a mano** al formulario.
- Un PDF multi-página (carrusel) cuenta como **1** pieza.

Fuente: `docs/research/linkedin-form-contract.md`, `docs/research/visuals-pipeline.md`.
