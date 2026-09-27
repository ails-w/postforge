# Disclaimers — lo que el generador NO puede afirmar

Fuente: `docs/adr/ADR-003-rag-per-project-vs-knowledge.md`, `docs/research/*`.

## Prohibiciones

| # | Prohibido | Por qué |
|---|---|---|
| 1 | Métricas que no estén en `brief.json` con cita | Falso y verificable en el repo |
| 2 | Tecnologías que no aparezcan en el repo | Quema credibilidad ante cualquiera que lo abra |
| 3 | Usuarios, clientes o resultados de negocio inventados | Daño reputacional/legal |
| 4 | «En producción» si el repo no lo demuestra | Verificable |
| 5 | Colaboradores no registrados en `projects.yaml` | LinkedIn les notifica la mención |
| 6 | Comparaciones despectivas con otras herramientas o personas | No aporta y expone |

## Regla de trazabilidad

Todo hecho del post y del formulario cita `archivo:línea` vía `brief.json`. El validador de Fase 2 bloquea hechos sin cita; el `critique` de Fase 3 los penaliza.

## Si falta evidencia

El generador escribe **menos**, no inventa. Un post corto con una prueba real vale más que un post largo con relleno.
