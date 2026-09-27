# Contrato del formulario «Añadir proyecto» (LinkedIn)

- **Fecha:** 2026-09-27
- **Estado:** snapshot
- **Fuente primaria:** capturas de la UI de LinkedIn aportadas por el autor (2026-09-26), formulario «Añadir proyecto».
- **Fuentes secundarias:** LinkedIn Help (ver §Fuentes).

## Campos (verificado en la UI)

| Campo | Obligatorio | Límite verificado | Notas |
|---|---|---|---|
| Nombre del proyecto | ✅ | 255 caracteres | contador visible en la UI |
| Descripción | — | 2.000 caracteres | contador visible en la UI |
| Aptitudes | — | «tus cinco aptitudes más relevantes» | aparecen también en la sección Aptitudes del perfil |
| Contenido multimedia | — | 50 elementos | imágenes, documentos, sitios web, presentaciones |
| Fecha de inicio | — | mes + año | |
| Fecha de finalización | — | mes + año | checkbox «Actualmente estoy trabajando en este proyecto» |
| Colaboradores | — | menciones | LinkedIn avisa a las personas mencionadas |
| Asociado con | — | selección única | empresa o institución educativa |

## Formatos de media soportados

LinkedIn Help, «Media file types supported on your profile» ([answer/a1516731](https://www.linkedin.com/help/linkedin/answer/a1516731), consultado 2026-09-27):

- Documentos: PDF `.pdf`, PowerPoint `.ppt/.pptx`, Word `.doc/.docx`
- Imágenes: `.jpg/.jpeg`, `.png`, `.gif` (sin animación: se extrae el primer frame)

Límites técnicos del mismo doc:

| Límite | Valor |
|---|---|
| Tamaño máximo de archivo | 100 MB |
| Páginas por documento | 300 |
| Palabras por documento | 1.000.000 |
| Resolución máxima de imagen | 120 megapíxeles |
| Subida de documentos desde móvil | No soportada |

Datos adicionales:

- El **campo URL del proyecto ya no existe** para proyectos nuevos: el enlace se agrega como media («Add media» → «Add a link»). Fuente: misma página de Help.
- Guías 2026 coinciden en que **PDF es el formato más confiable** para documentos/carruseles (LinkedIn convierte cada página en imagen).

## Implicaciones para postforge

1. `form.md` emite exactamente estos bloques, en este orden, listos para copiar: nombre · descripción · 5 aptitudes · fechas · colaboradores · asociado con.
2. Validaciones duras (fallan la salida, no son warnings):
   - `len(nombre) <= 255`
   - `len(descripcion) <= 2000`
   - `len(aptitudes) == 5`
   - `len(media) <= 50`
3. Fuente de verdad de los datos: `projects.yaml` (fechas, colaboradores, asociado con) + `brief.json` (nombre, descripción, aptitudes con evidencia).
4. El post del feed **no** es el formulario: el formulario guarda el proyecto; el post lo cuenta. Son dos artefactos distintos (`post.md` vs `form.md`).
5. Para la media: PDF/imagen generados por `visuals` (Fase 4), dentro de los límites de esta tabla.

## Qué NO entra en este contrato

| Tema | Doc |
|---|---|
| Cómo buscan los reclutadores, keywords, ATS | `recruiter-search-ats.md` |
| Ganchos, truncado del feed, psicología | `hooks-psychology.md` |
| Diagramas y portadas para la media | `visuals-pipeline.md` |

## Verificado vs pendiente

**Verificado:**

- Límites 255 / 2.000, 5 aptitudes, 50 elementos de media, campos de fecha/colaboradores/asociado (capturas UI, 2026-09-26).
- Formatos y límites técnicos de media (LinkedIn Help, 2026-09-27).
- No hay campo URL de proyecto (LinkedIn Help, 2026-09-27).

**Pendiente:**

- [ ] ¿La descripción acepta saltos de línea y emojis? (probar al pegar).
- [ ] ¿«Sitios web» como tipo de media sigue disponible en el selector? (cambió con el retiro del campo URL).
- [ ] Límite de peso/resolución específico por tipo de media **en el formulario de proyectos** (los límites hallados son del perfil general).

## Fuentes

| Fuente | Uso | Consultado |
|---|---|---|
| Capturas UI «Añadir proyecto» (autor) | campos y límites del formulario | 2026-09-26 |
| [linkedin.com/help/linkedin/answer/a1516731](https://www.linkedin.com/help/linkedin/answer/a1516731) | formatos y límites de media | 2026-09-27 |
| [linkedin.com/help/linkedin/answer/a564109](https://www.linkedin.com/help/linkedin/answer/a564109) | formatos de media generales | 2026-09-27 |
| [linkedin.com/help/linkedin/answer/a540837](https://www.linkedin.com/help/linkedin/answer/a540837) | flujo «Add profile section» | 2026-09-27 |
