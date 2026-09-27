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

- En el **formulario** (perfil): recomendado **2** (una principal + una de prueba). Máximo 3 en proyectos insignia. El formulario admite 50, la atención no.
- En el **post** (feed): **1 pieza** por defecto (ver flujo abajo).
- Se generan en `out/<slug>/<fecha>/media/` (local, gitignored) y se suben **a mano**.
- Un PDF multi-página (carrusel) cuenta como **1** pieza.

## Flujo de publicación (dos superficies)

```text
postforge gen <slug>
   ├── post.md        → se pega en «Crear publicación» (feed)
   ├── form.md        → se pega en Perfil → Añadir proyecto
   ├── media/         → se adjunta a mano (una sola vez)
   └── checklist.md   → pasos finales
```

### 1. Post del feed

- Texto: `post.md` (≤ 3.000 caracteres; el hook vive antes del corte de ~140).
- Media: **una sola elección** por post:
  - **Imagen** (default): 1 pieza (portada o diagrama). Hasta 20 imágenes por post; ratio máximo 4:5 (vertical).
  - **Documento PDF / carrusel** (opcional, proyectos insignia): 3-5 páginas (portada, diagrama, prueba). LinkedIn convierte cada página en imagen y se desliza.
  - **Video/GIF** (`vhs`, Fase 4).
- **No se mezcla**: documento + imágenes en el mismo post no es posible.
- El texto del post **no** es la descripción del formulario.

### 2. Formulario «Añadir proyecto»

- `form.md` completo: nombre, descripción (≤ 2.000), 5 aptitudes, fechas, colaboradores, asociado con.
- Media: hasta 50 elementos; acá sí conviven varias piezas (imagen + PDF + enlaces).
- Publicar el formulario **después** del post: el post trae la visita; el proyecto queda como evidencia permanente y buscable.
- **¿Es redundante?** No: el post distribuye (feed, primeras horas) y el formulario permanece (búsqueda). La única regla es no duplicar el texto literal. Fuente: `docs/research/recruiter-search-ats.md` §redundancia.

Fuente: LinkedIn Help `a527229` (multi-imagen, ratio 4:5), `a1516731` (formatos), `docs/research/visuals-pipeline.md`.
