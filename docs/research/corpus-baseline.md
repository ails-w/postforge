# Corpus baseline — 3 repos reales

- **Fecha:** 2026-09-27
- **Estado:** snapshot
- **Propósito:** validar el `ingest` y derivar los arquetipos y la taxonomía. Es un **oráculo humano**, no un input del runtime: en producción el scanner procesa cualquier repo.

## Por qué estos 3

Uno por familia, para que el ingest no se optimice a un solo formato:

| Repo | Familia / arquetipo | Dominio | Formato dominante | Git | Tamaño |
|---|---|---|---|---|---|
| `focusguard` | `iac-security` | Linux: PAM + systemd + integridad | bash (4) + markdown (22) + units (5) | sí | 42 archivos · 2.802 líneas |
| `focusblock` | `cli-systems` | C#/.NET: TUI + daemon | C# (64) + markdown (43) | sí | 120 archivos · 10.474 líneas |
| `db-deep-dive-portfolio` | `docs-data` | Bases de datos (DDIA) | markdown (50) | **no** | 50 archivos · 3.827 líneas |

## Hallazgos que se vuelven requisitos del ingest

### H1 — No asumir git

`db-deep-dive-portfolio` no tiene `.git`. El scanner necesita dos caminos: si hay repo → `git ls-files`; si no → walk del filesystem con exclusiones explícitas. Aplica también a zips descargados o copias a mano.

### H2 — Exclusiones mínimas

- Carpetas: `.git/`, `bin/`, `obj/`, `node_modules/`, `.venv/`, `out/`, `dist/`.
- `focusblock` tiene `bin/` y `obj/` en disco aunque estén ignorados por git: con git alcanza con `git ls-files`; sin git, la lista de exclusiones debe ser explícita.

### H3 — Doc-heavy vs code-heavy

- `focusguard`: 52 % markdown → el post se sostiene con README, módulos y diagramas.
- `focusblock`: 53 % C# → hay que leer código para extraer evidencia real (interfaces, tests, ADRs).
- `db-deep-dive-portfolio`: 100 % markdown → sin código, la evidencia son los análisis y los logs de desarrollo.

Regla: el brief pondera `README`/`docs/` para el relato y `código + tests` para la prueba.

### H4 — El README no es la verdad de los artefactos

El README de `db-deep-dive-portfolio` promete `schema.sql`, `seed-data.sql` y `queries.sql` por mini-proyecto, pero el repo tiene **0 archivos `.sql`**. Un extractor que confíe en el README afirmaría cosas que no existen.

Regla: todo hecho del brief cita un artefacto existente; las promesas del README no son evidencia (→ `knowledge/disclaimers.md`).

### H5 — Estructura numerada = metadata gratis

`focusguard/modules/00-base…04-disarm` y `db-deep-dive-portfolio/01-fundamentos…04-proyecto-final`: el número de carpeta es el orden narrativo. El chunker guarda `section` y `order` para reconstruir el relato.

### H6 — Formatos con estructura estable

| Patrón | Repo | Explotación determinista |
|---|---|---|
| `docs/adr/ADR-0NN-*.md` (Contexto/Decisión/Consecuencias) | focusblock | Extraer decisión + consecuencia |
| `modules/NN-*/README.md` + `apply.sh`/`verify.sh` | focusguard | Módulo = unidad narrativa |
| `docs/learning/phase-*.md` (glosario + conceptos) | focusblock | Conceptos pedagógicos citables |
| Units `.service` / `.timer` | focusguard | Unidades de configuración con semántica |
| `mini-*/analysis.md` + `ddia-reference.md` | db-deep-dive | Análisis → evidencia de dominio |

## Query set del baseline (Fase 1-2)

| Query | Repo | Qué debe recuperar |
|---|---|---|
| `pam_time` | focusguard | módulo `01-pam-gate` + `time.conf` |
| `chattr +i` | focusguard | módulo `03-integrity` |
| `Unix socket` | focusblock | `IpcServer`/`IpcClient` + ADR-002 |
| `early stop` | focusblock | `BlockEngine` + `ChallengeDialog` |
| `B-Tree vs LSM` | db-deep-dive | `mini-02-btree-vs-lsm` + `ddia-reference.md` |
| `isolation levels` | db-deep-dive | `mini-06-isolation-levels` + `analysis.md` |

Estas queries son la base de los golden files: respuesta esperada escrita a mano (oráculo) → `tests/fixtures/expected/`.

## Evidencia por repo (para el arquetipo)

### focusguard → `iac-security`

| Evidencia | Fuente |
|---|---|
| 5 capas independientes con nombre y propósito | `README.md` (tabla de capas) |
| El bug real del `pkill -KILL` (pantalla negra) | `README.md` §What I learned |
| Flujo de enforcement | `docs/diagrams/enforcement-flow.md` |
| Install / verify / rollback por módulo | `modules/*/README.md` |
| Estado: 4 módulos + base | `modules/` |

### focusblock → `cli-systems`

| Evidencia | Fuente |
|---|---|
| TUI ↔ daemon por Unix socket | `docs/architecture.md`, `docs/adr/ADR-002-ipc-unix-socket.md` |
| Tests y disciplina TDD | `tests/` (23 archivos), `docs/learning/` |
| Decisiones con contexto | `docs/adr/ADR-001…012` |
| Conceptos pedagógicos | `docs/learning/phase-*.md` |
| Gotchas de plataforma (.NET 10, Terminal.Gui) | `AGENTS.md` §Gotchas |

### db-deep-dive-portfolio → `docs-data`

| Evidencia | Fuente |
|---|---|
| Programa en 4 bloques + 9 mini-proyectos | `README.md`, carpetas `0N-*` |
| Análisis por mini-proyecto | `mini-*/analysis.md` |
| Referencias al libro (DDIA) | `mini-*/ddia-reference.md` |
| Progreso documentado | `mini-*/development-log.md` |
| Plantillas propias del autor | `docs/templates/` |
| SQL ejecutable | **No verificado**: 0 archivos `.sql` en el repo |

## Decisiones derivadas

- Arquetipos iniciales confirmados por corpus: `iac-security`, `cli-systems`, `docs-data`. (`backend-api` y `lib` quedan en el catálogo sin corpus todavía.)
- El scanner de Fase 1 implementa el fallback sin git (H1) como requisito, no como extra.
- El validador de Fase 2 bloquea hechos que citen artefactos inexistentes (H4).
- `projects.yaml` puede registrar repos sin git: el campo `path` no asume remoto.

## Golden files (Fase 1)

- `tests/fixtures/corpus/{focusguard,focusblock,db-docs}/` — recortes versionados.
- `tests/fixtures/expected/chunks-*.json` y `search-*.json` — escritos a mano a partir de este doc.
