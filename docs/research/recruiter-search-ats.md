# Cómo encuentran (y filtran) los reclutadores

- **Fecha:** 2026-09-27
- **Estado:** snapshot
- **Pregunta:** ¿cómo me encuentran y me filtran reclutadores y ATS?

## Resumen ejecutivo (5 reglas para el generador)

1. La búsqueda es **léxica y explícita**: si no nombrás la tecnología, no existís para el filtro.
2. El filtro **Skills and Assessments** existe como tal: las 5 aptitudes del proyecto alimentan la sección Skills del perfil.
3. Las keywords se **resaltan** en la profile card, el Summary, la Experience y Skills → repetir el término central en nombre + descripción + aptitudes.
4. Los reclutadores combinan sinónimos con OR → cubrir vocabulario ES/EN (taxonomía).
5. Un ATS hace **matching léxico** contra la oferta: gana el término exacto, no el creativo.

## Cómo busca LinkedIn Recruiter (fuente oficial)

LinkedIn Help, «Use Boolean to filter search results in Recruiter and Recruiter Lite» ([a415295](https://www.linkedin.com/help/recruiter/answer/a415295), actualizado hace 2 semanas al 2026-09-27):

| Mecánica | Detalle |
|---|---|
| Filtros tratados como Boolean | Job titles, Location, Companies, **Skills and Assessments**, Schools, Industries, Spoken languages |
| Operadores | `NOT`, `OR`, `AND`, paréntesis. Los `+` y `-` **no** están soportados oficialmente |
| Dropdowns | **Must have** = AND · **Can have** = OR · **Doesn't have** = NOT |
| Dónde se resaltan las keywords | profile card, `Summary`, `Experience` (header, description, location) y **`Skills`** |
| Stop words ignoradas en `Keywords` | and, or, the, of, at, by, to, for, with, in, they, have, from, not, but, after |
| Filtro `Project` | **No soporta Boolean** (se bloquea un término con el icono Block) |
| Consejo oficial | «ser específico e inclusivo, no vago y exclusivo»: títulos relacionados + skills esenciales |

## Herramientas de sourcing externas

| Herramienta | Qué hace | Implicación para el post |
|---|---|---|
| SeekOut, HireEZ, Apollo, Lusha | Búsqueda y enriquecimiento de perfiles a escala | Tu perfil público es la fuente; proyectos visibles y con keywords correctas |

Contexto: estas herramientas operan sobre datos públicos y LinkedIn restringe el scraping en sus términos de uso. No es una palanca que postforge use; importa porque explica por qué el perfil indexado gana peso.

## Cómo filtra un ATS

| Mecánica | Detalle | Fuente |
|---|---|---|
| Parseo | NLP sobre el CV/perfil, indexado con un índice invertido para búsqueda instantánea | Jobscan |
| Scoring | Keywords del job description; matching léxico exacto primero | Jobscan / scale.jobs |
| Cobertura | Los análisis recomiendan cubrir los **15-35 requisitos principales** del puesto | JobWizard |
| Sinónimos | Dependen de la configuración del ATS; no los asumas | Jobscan |

## Traducción a reglas de postforge

| Regla | Dónde se aplica |
|---|---|
| Nombrar tecnología y versión («PostgreSQL 16», no «base de datos») | `brief` → `post.md`, `form.md` |
| Un término por sinónimo relevante ES/EN | `knowledge/keyword-taxonomy.yaml` |
| Repetir el término central en nombre + descripción + aptitudes | `form.md` (validación) |
| Verbos de logro + métrica | `knowledge/rubric.md` |
| Prohibido usar keywords de cosas no hechas | `knowledge/disclaimers.md` |

## ¿Es redundante publicar el post y cargar el proyecto en el perfil?

No: son dos mecanismos distintos sobre el mismo hecho.

| Superficie | Mecanismo | Vida útil |
|---|---|---|
| Post del feed | Distribución temporal: tu red, el feed, las primeras horas | Días |
| Sección Proyectos | Búsqueda y evaluación: queda en tu perfil, alimenta Skills | Permanente |

- Cargar proyectos está recomendado de forma consistente por guías de carrera (Resume Worded, Teal) y por contenido de LinkedIn: «un proyecto documentado rinde más que meses de publicaciones genéricas» (opinión de industria, no dato oficial).
- **No se encontró evidencia de penalización** por publicar y además cargar el proyecto; el riesgo es de forma, no de algoritmo.
- El único riesgo real es **duplicar el texto literal**: el post es narrativa (atención) y el formulario son hechos buscables (búsqueda). Mismo hecho, distinta forma.
- Recomendación derivada: publicar el post primero y cargar el proyecto el mismo día. No compiten: se acumulan.

## Honestidad / límites

- LinkedIn **no publica** el scoring de su búsqueda; lo documentado son filtros, operadores y dónde se resaltan keywords.
- El SEO de perfil no reemplaza evidencia: el objetivo es ser **encontrable por lo que realmente hiciste**, no inflar términos.
- El filtro `Project` no soporta Boolean: los proyectos probablemente pesan vía Skills y keywords del perfil, no como campo de búsqueda avanzada.

## Fuentes

| Fuente | Uso | Consultado |
|---|---|---|
| [LinkedIn Help Recruiter a415295](https://www.linkedin.com/help/recruiter/answer/a415295) | Boolean, filtros, resaltado de keywords, stop words | 2026-09-27 |
| [Jobscan — ATS](https://www.jobscan.co/blog/8-things-you-need-to-know-about-applicant-tracking-systems/) | parsing NLP + índice invertido | 2026-09-27 |
| [JobWizard — keyword scoring](https://jobwizard.ai/blog/ats-resume-optimization-part-2-keyword-matching-deep-dive-and-scoring-algorithm-explained) | cobertura de 15-35 requisitos | 2026-09-27 |
| [SeekOut — guía Boolean](https://www.seekout.com/blog/the-definitive-guide-to-boolean-searches-for-recruiters/) | prácticas de sourcing | 2026-09-27 |
