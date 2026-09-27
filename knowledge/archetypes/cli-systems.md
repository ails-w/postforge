# Arquetipo — CLI y herramientas de sistema

> Base común: `hooks-psychology.md`, `recruiter-ats.md`, `linkedin-form.md`.
> Detección automática: `write/archetype.py` (Fase 3).

## Señales (detección)

- `bin/`, `scripts/`, `src/*/cli.py`, `cmd/`, subcomandos Typer/argparse/Cobra.
- Daemon + IPC, units `.service`/`.timer`, scripts con `set -euo pipefail`.
- Tests centrados en flags, parsing y casos límite.

## Hook recomendado

Fórmulas: **métrica** o **error confesado**. El CLI ya tiene números (tiempo, pasos, flags); usarlos.

Forma: «Este script tardaba N en X; el cuello era Y» / «Reduje el setup de A pasos a B».

## Prueba que importa

| Prueba | De dónde sale |
|---|---|
| Antes/después de un comportamiento | README, learning docs |
| Tests y casos límite | `tests/`, CI |
| Nº de subcomandos o módulos | Código |
| Tiempo de ejecución | Solo si está medido en el repo |

## Media

| Pieza | Formato | Por qué |
|---|---|---|
| Principal | GIF de terminal (`vhs`) | Muestra la herramienta trabajando |
| Secundaria | Diagrama de componentes (`mmdc`) | Explica la arquitectura |

## Aptitudes típicas (taxonomía)

`python-cli` (Python, Typer, pytest) · `sistemas-linux` (Bash, systemd) · `devops` (Git, CI).

## Descripción del formulario

Problema (1 línea) → qué hace (2-3) → stack nombrado (1) → prueba (1).

## Evitar

- Pegar la salida de `--help`.
- Listar flags sin contar qué problema resuelven.

## Ejemplos del autor

`focusblock` (TUI + daemon) · `postforge` (este CLI) · `dns-doh-lockdown` (scripts de instalación).
