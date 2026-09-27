# Fase 0 — Setup, research y spikes

> Qué se aprende en esta fase y por qué importa.
> Log de la fase → `docs/progress-log/phase-00-setup.md`
> Concepto transversal (uv) → `docs/learning/uv.md`

## Glosario de la fase

| Término | Qué significa (en una línea) |
|---|---|
| **Lockfile** | Versiones exactas + hashes de todas las dependencias (`uv.lock`) |
| **`--frozen`** | Modo «no resuelvas, falla si el lock no coincide» (CI) |
| **JSONL** | Texto donde cada línea es un JSON completo |
| **Evento** | Un mensaje del stream de `opencode run --format json` |
| **`sessionID`** | Identificador que permite continuar una conversación (`--session`) |
| **Embedding** | Vector de números que representa el significado de un texto |
| **Similitud coseno** | Medida de parecido entre dos vectores (−1 a 1) |
| **Chunk** | Fragmento de documento que se indexa como unidad |
| **Búsqueda híbrida** | Fusión de léxica (palabras exactas) + semántica (significado) |
| **Seam** | Punto de inyección para reemplazar una dependencia en tests |

## Mapa de conceptos

```text
uv (transversal) ──► entorno reproducible ──► CI reproducible
                                                    │
salida estructurada del LLM ──► llm.py ──► pipeline que puede fallar ruidoso
                                                    │
embeddings ──► búsqueda semántica ──┐
                                    ├──► búsqueda híbrida (Fase 2)
FTS5 / BM25 (Fase 1) ───────────────┘
```

## Puntos de inyección de la fase

| Componente | Seam | Doble | Test real |
|---|---|---|---|
| LLM | `LlmClient` | `FakeLlm` | `opencode run` (local, smoke) |
| Proceso | `CommandRunner` | `FakeRunner` | subprocess real |
| Embeddings (Fase 2) | `Embedder` | `FakeEmbedder` | fastembed local |
| Filesystem | `Path` por parámetro | `tmp_path` | fixtures del oráculo |

---

## Salida estructurada de un LLM por CLI

### En una frase

Pedir la respuesta del modelo en un formato fijo convierte su texto en algo que el código puede verificar.

### Fundamentos previos

**JSON** es un formato de datos con llaves-valor. **JSONL** es una lista de JSON, uno por línea. Un proceso tiene **stdout** (salida normal), **stderr** (errores) y un **exit code** (0 = éxito).

### Qué es

`opencode run --format json` no devuelve prosa: emite un **stream de eventos** JSONL. Cada evento tiene un `type`; el texto del modelo llega en `part.text` de los eventos `type=text`; todos traen `sessionID`.

### Qué problema resuelve

Sin contrato, «parsear» la respuesta dependría de heurísticas sobre texto libre: frágil e imposible de testear. Con contrato, se valida y si algo no calza, **falla ruidoso** en vez de seguir con datos sucios.

### Cómo funciona paso a paso

1. `llm.py` construye el argv: `opencode run -m <modelo> --format json "<prompt>"`.
2. El `CommandRunner` lo ejecuta y captura stdout/stderr/exit code.
3. `parse_events` recorre línea por línea: vacías se ignoran, malformadas lanzan `LlmError`.
4. Los textos se concatenan; el `sessionID` se conserva.
5. El resultado (`LlmResult`) es lo único que ve el pipeline.

### Qué se rompería sin esto en postforge

El `brief.json` dependería de «entender» prosa: hechos sin cita, JSON inválido y errores silenciosos a mitad del pipeline.

### Cómo se usa (código real)

```python
from postforge.llm import OpenCodeLlm

llm = OpenCodeLlm()
result = llm.complete("Reply with exactly: ok", model="opencode-go/deepseek-v4.1-flash")
print(result.text, result.session_id)
```

### Error común

Asumir que cada evento contiene la respuesta completa, o que stdout es siempre JSON. El spike real (ADR-005) documenta una salida normal, pero el parser trata cada línea como un evento independiente.

### Para profundizar

- `docs/adr/ADR-005-models-and-json-contract.md` — contrato observado y precios.
- `tests/test_llm.py` — 11 tests del contrato.

---

## Embeddings y búsqueda híbrida

### En una frase

Un embedding convierte texto en un vector donde «significado parecido» es «vector cercano».

### Fundamentos previos

Un **vector** es una lista de números. **Coseno** mide el ángulo entre dos vectores (≈1 = misma dirección). Un **chunk** es el fragmento que se indexa.

### Qué es

Un modelo de embeddings (ej. MiniLM multilingüe) mapea un texto a 384 números. Textos con significados similares quedan cerca aunque no compartan palabras.

### Qué problema resuelve

Buscar «¿cómo evito que alguien entre fuera de horario?» y encontrar el módulo PAM aunque el README diga «gate» y no «entrar». El léxico no cubre paráfrasis.

### Cómo funciona paso a paso

1. Cada chunk se convierte en vector al indexar.
2. La consulta se convierte en vector con el **mismo** modelo.
3. Se calcula coseno contra todos los vectores y se toman los top-k.

### Qué se rompería sin esto en postforge

El brief solo encontraría coincidencias de palabras exactas; preguntas naturales en español se perderían.

### Cómo se usa (código real)

```bash
uv run --with fastembed python scripts/spike_embeddings.py \
  --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Error común

Creer que los embeddings reemplazan la búsqueda léxica. El spike mostró scores bajos (0,13-0,43) en fragmentos cortos: **la fusión con FTS5/BM25 es obligatoria** (ADR-004). Otro clásico: usar la familia e5 sin sus prefijos `query:` / `passage:`.

### Para profundizar

- `docs/adr/ADR-004-embeddings-model.md` · `scripts/spike_embeddings.py`.

---

## CI con lockfile congelado

### En una frase

El CI no resuelve dependencias: reproduce exactamente el entorno del lock y falla si no coincide.

### Fundamentos previos

CI = máquinas que corren tus checks en cada push/PR. `--frozen` = «no toques el lock; si no cuadra, abortá».

### Qué es

`.github/workflows/ci.yml`: instala uv → `uv python install` → `uv sync --frozen` → `ruff check` → `ruff format --check` → `pytest -m "not integration"`.

### Qué problema resuelve

La clase de bug más cara: «en mi máquina funciona». Sin lock congelado, cada máquina resuelve versiones distintas y los tests verdes locales no dicen nada.

### Cómo funciona paso a paso

1. `setup-uv` instala uv (versión pinneada por commit) y habilita caché.
2. `uv python install` baja el intérprete del `.python-version`.
3. `uv sync --frozen` verifica el lock y crea el entorno.
4. Ruff y pytest corren **desde ese entorno** (`uv run`).
5. Los tests marcados `integration` quedan afuera: el CI no llama al LLM ni descarga modelos.

### Cómo se usa (código real)

```yaml
- run: uv sync --frozen
- run: uv run pytest -m "not integration"
```

### Error común

Commitear código sin `uv.lock` (o con el lock viejo): el CI falla por diseño, y eso es correcto — el lock es parte del código.

### Para profundizar

- `.github/workflows/ci.yml` · `docs/learning/uv.md` (concepto transversal).

---

## Relación entre estos conceptos

`uv` (transversal) garantiza que cada máquina tenga el mismo entorno; el CI lo verifica. La salida estructurada del LLM es el contrato que hace testeable al pipeline. Los embeddings se medirán con el léxico en la Fase 2: ninguno de los dos se usa solo. Orden de dependencia: **entorno → contrato → recuperación**.
