# Arquetipo — Infraestructura, configuración y seguridad

> Base común: `hooks-psychology.md`, `recruiter-ats.md`, `linkedin-form.md`.

## Señales (detección)

- Módulos numerados (`modules/00-base`, `01-…`), `install.sh` / `verify.sh` / `uninstall.sh`.
- Configuración del sistema: PAM, nftables, systemd, DNS, `chattr`, políticas.
- Docs de amenaza/verificación (`threat-model.md`, `verification.md`) y rollback documentado.

## Hook recomendado

Fórmula: **error confesado** o **contraste**. La historia está en el modo de fallo.

Forma: «Bloquear por horario es fácil de hacer a medias: X no cubre Y. Necesitás Z.»

## Prueba que importa

| Prueba | De dónde sale |
|---|---|
| Modo de fallo real (bug encontrado) | README §What I learned, learning docs |
| Capas independientes y su porqué | README, módulos |
| Verificación reproducible | `verify.sh`, tests de host |
| Rollback / desarme auditado | Módulos de disarm |

## Media

| Pieza | Formato | Por qué |
|---|---|---|
| Principal | Diagrama de capas o flujo (`mmdc`) | Explica el modelo de defensa |
| Secundaria | Config antes/después (snippet de texto) | Prueba concreta del cambio |

## Aptitudes típicas (taxonomía)

`sistemas-linux` (Linux, PAM, systemd, nftables, Bash) · `devops` (Git, ADRs) · `documentacion`.

## Descripción del formulario

Modo de fallo (1 línea) → capas que lo cubren (2-3) → stack del sistema (1) → verificación (1).

## Evitar

- Vender «seguridad invulnerable»: estos proyectos prometen honestidad («gate deliberado, revertible y auditado»).
- Logs como prueba visual.

## Ejemplos del autor

`focusguard` (PAM + enforcement + integridad) · `battery-guard` (control de carga) · `dns-doh-lockdown` (DNS + firewall + políticas).
