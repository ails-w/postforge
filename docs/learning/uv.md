# uv — entorno reproducible y proyecto Python

> Concepto **transversal** (no pertenece a una fase): es la herramienta base de todo el proyecto.
> Se referencia desde `docs/learning/phase-00-setup.md` y desde `AGENTS.md`.
> Herramienta instalada: `uv 0.12.18` (verificado 2026-09-27).

## Glosario

| Término | Qué significa (en una línea) |
|---|---|
| **Paquete** | Código distribuible con metadata (nombre, versión, dependencias) |
| **Dependencia** | Paquete del que depende tu proyecto o que tu proyecto usa |
| **Restricción / rango** | Lo que declarás en `pyproject.toml` (`typer>=0.16`): "quiero cualquiera ≥ 0.16" |
| **Resolución** | Elegir UNA combinación de versiones que satisfaga todos los rangos |
| **Lockfile** (`uv.lock`) | El resultado congelado de la resolución: versiones exactas + hashes |
| **Entorno virtual** (`.venv/`) | Carpeta con un intérprete y paquetes aislados del sistema |
| **Caché** (`~/.cache/uv/`) | Paquetes descargados una vez; se reutilizan por hardlinks |
| **wheel / sdist** | Paquete precompilado / código fuente para compilar |
| **Editable install** | Tu propio proyecto instalado "vivo": los cambios se reflejan sin reinstalar |
| **PEP 621** | El estándar del bloque `[project]` de `pyproject.toml` |

## Mapa de conceptos

```text
pyproject.toml            uv.lock                    .venv/
(rangos: "typer>=0.16")   (versiones exactas         (intérprete Python 3.12
        │                  + hashes, commiteado)      + paquetes instalados)
        │                        │                          ▲
        └────── uv lock ─────────┘                          │
                                                           │
   uv sync ── reconcilia el entorno con el lock ───────────┘
   uv run ─── ejecuta un comando del entorno (sin activar nada)
   uv python install 3.12 ── instala el intérprete que usa el proyecto
```

---

## Concepto 1 — Paquete, dependencia y resolución

### En una frase

Una dependencia es una promesa con rango; la resolución la convierte en versiones exactas.

### Fundamentos previos

`pyproject.toml` es un archivo TOML donde vive la metadata del proyecto: el bloque `[project]` declara nombre, versión, `requires-python` y `dependencies`. Los **rangos** (`>=`, `~=`) permiten recibir mejoras sin romper compatibilidad.

### Qué es

La resolución es el proceso de elegir una versión concreta por paquete que cumpla **todos** los rangos a la vez, incluidas las dependencias de las dependencias (grafo transitivo).

### Qué problema resuelve

Sin resolución, dos máquinas instalan versiones distintas y aparece el clásico «en mi máquina funciona».

### Cómo funciona paso a paso

1. uv lee los rangos de `pyproject.toml`.
2. Consulta el índice (PyPI) y construye el grafo de dependencias transitivas.
3. Descarta combinaciones incompatibles (`requires-python`, extras, plataforma).
4. Escribe el resultado en `uv.lock`: versiones exactas + hashes de descarga.
5. En cada `uv sync`, el lock manda: no se vuelve a resolver si sigue satisfechо.

### Qué se rompería sin esto en postforge

El CI y tu máquina podrían usar versiones distintas de Typer/Pydantic; los tests pasarían local y fallarían en CI (o al revés) sin que nadie tocara el código.

### Cómo se usa (código real)

```toml
# pyproject.toml (postforge)
[project]
requires-python = ">=3.12"
dependencies = ["typer>=0.16", "pydantic>=2.9", "pyyaml>=6.0", "rich>=13.9", "jinja2>=3.1"]
```

### Error común

Creer que `>=` fija la versión mínima **instalada**. No: declara una compatibilidad; la versión real la fija el lock.

### Para profundizar

- `uv.lock` se **commitea**; `.venv/` no.
- Docs: https://docs.astral.sh/uv/concepts/projects/layout/

---

## Concepto 2 — Entorno virtual

### En una frase

Un entorno virtual es un Python propio con sus paquetes, sin tocar el del sistema.

### Fundamentos previos

Cuando hacés `import typer`, Python busca el paquete en las carpetas de `site-packages` del intérprete que está corriendo. Si instalás todo en el intérprete del sistema, cualquier proyecto puede romper a otro.

### Qué es

Una carpeta `.venv/` con un enlace/copia del intérprete, su `pyvenv.cfg` y su propio `site-packages`.

### Qué problema resuelve

Aislamiento: el postforge de hoy y el de dentro de seis meses no contaminan tu Arch.

### Cómo funciona paso a paso

1. `uv sync` crea `.venv/` si no existe (usando el Python del proyecto).
2. Resuelve el lock y materializa cada paquete dentro de `.venv/lib/python3.12/site-packages`.
3. `uv run` ejecuta con ese intérprete vía `PATH`/`VIRTUAL_ENV`, sin que actives nada.
4. Tu proyecto se instala en modo *editable*: `postforge` apunta a `src/postforge/`.

### Qué se rompería sin esto en postforge

Instalar Typer en el Python 3.14 del sistema haría fallar otras herramientas; y `postforge` dependería del estado global de la máquina.

### Cómo se usa (código real)

```bash
uv sync                      # crea/actualiza .venv con el lock
uv run postforge --help      # ejecuta DENTRO del entorno
source .venv/bin/activate    # opcional: activarlo (no necesario con uv)
```

### Error común

Ejecutar `python script.py` en vez de `uv run python script.py`. El primero usa el Python del sistema (3.14, sin wheels) y falla con cosas crípticas.

### Para profundizar

- https://docs.astral.sh/uv/concepts/projects/layout/

---

## Concepto 3 — Versiones de Python

### En una frase

uv administra también los intérpretes: el proyecto declara cuál quiere y uv lo consigue.

### Fundamentos previos

En Linux, `python3` apunta a lo que decidió la distro (acá 3.14.7). Cambiar el global es mala idea; usar otro intérprete por proyecto es la solución sana.

### Qué es

`uv python install 3.12` descarga un Python manejado por uv (a `~/.local/share/uv/python/`) sin tocar el del sistema. El archivo `.python-version` ancla la versión del proyecto.

### Qué problema resuelve

Este proyecto **necesita 3.12** porque 3.14 aún no tiene wheels de torch/chromadb/sqlite-vec. Sin gestión de versiones, el proyecto sería irreproducible en tu máquina y en CI.

### Cómo funciona paso a paso

1. `.python-version` y `requires-python` declaran el objetivo.
2. Si no existe el intérprete, `uv sync`/`uv run` lo instala o lo descarga solo.
3. En CI, `uv python install` lo hace explícito y cacheable.

### Qué se rompería sin esto en postforge

`uv sync` usaría el 3.14 del sistema y fallaría al resolver (o peor: funcionaría hasta que agreguemos fastembed/sqlite-vec en Fase 2).

### Cómo se usa (código real)

```bash
cat .python-version     # 3.12
uv python install 3.12  # explícito (lo hace el CI)
uv python list          # ver todos los intérpretes disponibles
```

### Error común

Poner `requires-python = ">=3.14"` por usar el del sistema. La regla acá es la inversa: el proyecto fija 3.12 y uv lo trae.

---

## Concepto 4 — Ejecución y punto de entrada

### En una frase

`uv run` es el «doble clic» del proyecto: garantiza que todo corre con el entorno correcto.

### Fundamentos previos

Un *entry point* es un comando que el paquete expone. Se declara en `[project.scripts]` y queda disponible dentro del entorno.

### Qué es

```toml
[project.scripts]
postforge = "postforge.cli:main"
```

significa: «el comando `postforge` llama a la función `main()` de `postforge/cli.py`».

### Qué problema resuelve

Elimina el «¿activé el venv?». `uv run postforge gen focusguard` funciona siempre, en cualquier terminal, y es exactamente lo que ejecuta el CI.

### Cómo funciona paso a paso

1. `uv run` verifica que el entorno coincida con el lock (y lo sincroniza si no).
2. Ejecuta el comando con el Python del proyecto.
3. El entry point resuelve el import y llama a `main()`.

### Qué se rompería sin esto en postforge

Habría que documentar activación del venv, `PYTHONPATH=src`, y cada usuario tendría su método; los comandos del README y del CI divergirían.

### Cómo se usa (código real)

```bash
uv run postforge --help
uv run pytest
uv run ruff check .
```

### Error común

Poner lógica ejecutable en `if __name__ == "__main__"` del paquete y omitir `[project.scripts]`. El entry point es el contrato.

---

## Concepto 5 — Caché

### En una frase

uv descarga cada paquete una sola vez y lo reutiliza por hardlinks: por eso instala en milisegundos.

### Fundamentos previos

Un hardlink son dos rutas al mismo contenido en disco (sin duplicar bytes).

### Qué es

`~/.cache/uv/` guarda wheels/sdists descomprimidos y verificados por hash.

### Qué problema resuelve

Recrear entornos es barato: `.venv/` se puede borrar y reconstruir sin volver a descargar.

### Cómo funciona paso a paso

1. Descarga el paquete (si no está) a la caché y verifica el hash del lock.
2. Crea un hardlink dentro de `.venv/.../site-packages`.
3. Borrar `.venv/` no borra la caché; el próximo `uv sync` es instantáneo.

### Qué se rompería sin esto en postforge

Cada `uv sync` en CI bajaría todo de nuevo (por eso el CI habilita `enable-cache: true`).

### Error común

Borrar `~/.cache/uv` «para ahorrar lugar» y luego quejarse de que tarda; o depurar corrupción sin probar `uv cache clean`.

---

## Concepto 6 — Herramientas efímeras y `--with`

### En una frase

Podés usar un paquete sin agregarlo al proyecto: existe solo durante ese comando.

### Fundamentos previos

Hay dos tipos de dependencias: las del **proyecto** (van al lock) y las de una **corrida puntual** (no).

### Qué es

- `uvx <herramienta>`: ejecuta una herramienta aislada (equivalente a `pipx run`).
- `uv run --with fastembed python ...`: añade un paquete solo a esa ejecución.

### Qué problema resuelve

Spikes y herramientas (una medición, un linter puntual) no contaminan `pyproject.toml` con dependencias que quizá nunca uses.

### Cómo se usa (código real)

```bash
uv run --with fastembed python scripts/spike_embeddings.py --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Así se hizo el spike de embeddings (ADR-004) sin agregar `fastembed` al proyecto: recién en Fase 2, si gana, pasa a dependencia real.

### Error común

Agregar al proyecto (`uv add`) una librería que se usa una vez. La regla: si el código del paquete la importa, `uv add`; si es un experimento, `--with` o `uvx`.

---

## Comandos esenciales

| Comando | Qué hace |
|---|---|
| `uv sync` | Reconciliar `.venv` con `uv.lock` |
| `uv sync --frozen` | Igual, pero **falla** si el lock no está al día (CI) |
| `uv run <cmd>` | Ejecutar dentro del entorno |
| `uv add <pkg>` | Agregar dependencia (+ lock + entorno) |
| `uv add --dev <pkg>` | Dependencia de desarrollo |
| `uv remove <pkg>` | Quitar dependencia |
| `uv lock` | Resolver y escribir/actualizar el lock |
| `uv lock --upgrade` | Actualizar versiones permitidas por los rangos |
| `uv lock --upgrade-package <pkg>` | Actualizar solo una dependencia |
| `uv python install 3.12` | Instalar/descargar un intérprete |
| `uv venv --python 3.12` | Crear entorno a mano (normalmente no hace falta) |
| `uv tree` | Árbol de dependencias resuelto |
| `uv export --format requirements-txt` | Exportar el lock para herramientas viejas |
| `uvx <tool>` | Ejecutar herramienta efímera |
| `uv tool install <tool>` | Instalar herramienta persistente |
| `uv run --with <pkg> <cmd>` | Dependencia efímera para un comando |
| `uv cache dir` / `uv cache clean` | Ver / limpiar caché |
| `uv self update` | Actualizar uv |

## Flujos típicos en postforge

```bash
uv sync                              # 1. preparar el entorno
uv add <nueva-dependencia>           # 2. agregar deps (actualiza pyproject + lock)
uv lock --upgrade-package pydantic   # 3. actualizar una sola por seguridad
uv run pytest                        # 4. día a día
uv run --with fastembed ...          # 5. spikes sin contaminar el proyecto
```

## Errores comunes (meta)

| Error | Síntoma | Corrección |
|---|---|---|
| Usar `python` del sistema | `ModuleNotFoundError` o fallas raras de wheels | `uv run python ...` |
| No commitear `uv.lock` | CI resuelve versiones distintas | `git add uv.lock` |
| Editar `uv.lock` o `.venv/` a mano | Hash mismatch, cosas fantasma | `uv sync` (regenera) |
| `pip install` dentro del proyecto | Paquete fuera del lock, CI no lo ve | `uv add` |
| Esperar que `uv sync` actualice versiones | Nada cambia | `uv lock --upgrade` |
| CI con `--frozen` y lock viejo | Falla al sincronizar | Commitear el lock |

## Cómo se usa en postforge

```bash
uv sync          # entorno
uv run postforge --help
uv run pytest -m "not integration"
```

CI (`.github/workflows/ci.yml`): `uv python install` → `uv sync --frozen` → `ruff` → `pytest`.

## Para profundizar

- Documentación oficial: <https://docs.astral.sh/uv/>
- Proyectos y layout: <https://docs.astral.sh/uv/concepts/projects/layout/>
- Integración con GitHub Actions: <https://docs.astral.sh/uv/guides/integration/github/>
- Concepto relacionado: `docs/learning/template-phase.md` (estructura de conceptos).
