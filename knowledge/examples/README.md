# Examples — posts de referencia (few-shot)

## Estado

Vacío a propósito: se llena con **posts reales publicados** a partir del piloto (`focusguard`). Hasta entonces solo existe `template-example.md`.

No se inventan ejemplos: un few-shot con datos falsos contamina la salida del generador.

## Formato de un ejemplo

`NN-slug.md` con:

- **Contexto**: repo, arquetipo, fecha.
- **Post**: el texto exacto publicado.
- **Por qué funciona**: 2-4 bullets citando la regla que cumple (`hooks-psychology.md`, `recruiter-ats.md`).
- **Resultado**: cuando exista, métricas reales (impresiones, visitas al perfil). Nunca estimadas.

## Uso en el pipeline

`prompts/write-post.md` toma hasta 3 ejemplos del mismo arquetipo como few-shot. Sin ejemplos, escribe solo con las reglas.
