# Diagramas

Solo crear archivos aquí si es necesario documentar visualmente:
- Flujo de datos entre componentes (ingesta → índice → brief → post)
- Diagrama de secuencia (las 3 llamadas al LLM)
- Diagrama de componentes (qué depende de qué)
- Flujo de una corrida completa (`index` → `brief` → `gen` → `visuals`)

## Índice

| Fase | Archivo | Contenido |
|---|---|---|
| 0 — Setup | — | Sin diagrama: la fase no tiene flujo de runtime que valga la pena dibujar. |
| 1 — Ingesta | `phase-01-ingest.md` | Scanner → chunker → store (qué produce cada paso). |
| 2 — Comprensión | `phase-02-understand.md` | Recuperación híbrida + map-reduce con citas. |
| 3 — Redacción | `phase-03-write.md` | brief + knowledge → variantes → rúbrica → artefactos. |
| 4 — Visuales | `phase-04-visuals.md` | Pipeline de media y render Mermaid → PNG. |

## Formatos

- **ASCII art** — Para diagramas simples en terminal/markdown
- **Mermaid** — Para diagramas más complejos (renderiza en GitHub)

## Regla

No crear diagramas por crear. Solo si algo es difícil de explicar con texto.

> Bonus: estos diagramas son a la vez **corpus de prueba** de `postforge visuals`
> (Mermaid → PNG), así que mantenerlos en Mermaid tiene doble propósito.
