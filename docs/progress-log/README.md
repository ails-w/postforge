# Progreso por Fase (Log)

Log HISTÓRICO de desarrollo por fase. Backup manual del estado + historial de decisiones, problemas y métricas.

> Estado ACTUAL (fase activa, próximo paso) → `docs/handoff.md`
> Conceptos aprendidos → `docs/learning/phase-NN-name.md`

## Archivos

| Fase | Archivo | Estado |
|------|---------|--------|
| 0 | `phase-00-setup.md` | ⏳ |
| 1 | `phase-01-ingest.md` | ⏳ |
| 2 | `phase-02-understand.md` | ⏳ |
| 3 | `phase-03-write.md` | ⏳ |
| 4 | `phase-04-visuals.md` | ⏳ |

## Cómo Usar

Al **cerrar cada fase** (y opcionalmente al cerrar una sesión de desarrollo):

1. Actualizar el log de la fase actual con el progreso.
2. Marcar tareas completadas con `[x]` y fecha.
3. Documentar decisiones tomadas y por qué.
4. Documentar problemas y soluciones.
5. Actualizar métricas (tests escritos, cobertura).

## Plantilla

Usar `template-phase.md` (en esta carpeta) para cada fase nueva.

## Relación con Engram

Estos archivos son backup manual. Engram es la fuente primaria de contexto entre sesiones. Si Engram no está disponible, estos archivos dan contexto mínimo para continuar.
