# Plan de Desarrollo — postforge

> Estrategia de testing, seams y CI. Los comandos viven en `AGENTS.md` (no se duplican acá).

## Pirámide de testing

| Nivel | Qué cubre | Dónde corre |
|---|---|---|
| Unit (por defecto) | Toda la lógica, con fakes de LLM/embeddings/FS | CI |
| Golden files | Ingesta y recuperación sobre el corpus baseline | CI |
| Integración local | `opencode run` real y embeddings reales (`@pytest.mark.integration`) | Solo en local, nunca CI |

## Seams (puntos de inyección)

| Dependencia | Seam | Doble en unit | Test real |
|---|---|---|---|
| LLM | protocolo `LlmClient` | `FakeLlm` con respuestas canónicas | `opencode run` (local) |
| Embeddings | protocolo `Embedder` | `FakeEmbedder` (vectores deterministas) | fastembed (local) |
| Filesystem | `Path` por parámetro | `tmp_path` de pytest | corpus baseline |
| Git | `list_tracked_files(path)` | lista fija en el test | `git ls-files` |

Regla: si algo no se puede testear sin red, es un seam que falta — se inyecta, no se parchea.

## Fixtures

- `tests/fixtures/corpus/` — recortes de los 3 repos de `docs/research/corpus-baseline.md` (bash/C#/docs).
- `tests/fixtures/expected/` — golden files: chunks esperados, resultados de búsqueda, brief canónico.
- Regla: si un golden cambia, el cambio se revisa a mano en el mismo commit.

## CI (GitHub Actions)

1. `uv sync`
2. `ruff check .`
3. `ruff format --check .`
4. `pytest -m "not integration"`

El CI no descarga modelos ni llama al LLM: si un test necesita uno de los dos, está mal clasificado.

## Convenciones de tests

- pytest; nombres `test_<unidad>_<condición>_<resultado_esperado>`.
- Sin mocks de librerías internas: los dobles entran por protocolo.
- Un test = una razón para fallar; comparaciones exactas antes que `assert x` genéricos.
