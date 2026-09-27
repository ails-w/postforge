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

## Oráculo de ingesta (golden files)

El ingest se valida contra **2 repos reales y en curso** (`focusguard`, `focusblock`) — no contra todos los proyectos. El oráculo es una lista escrita a mano de qué debe encontrar el scanner; sin él, los tests solo afirman lo que el código hace, no lo correcto.

| Repo | Familia | Query | Debe recuperar |
|---|---|---|---|
| focusguard | `iac-security` | `pam_time` | `modules/01-pam-gate` + `time.conf` |
| focusguard | `iac-security` | `chattr +i` | `modules/03-integrity` |
| focusblock | `cli-systems` | `Unix socket` | `IpcServer`/`IpcClient` + ADR-002 |
| focusblock | `cli-systems` | `early stop` | `BlockEngine` + `ChallengeDialog` |

- Fixtures: `tests/fixtures/corpus/{focusguard,focusblock}/` (recortes) + `tests/fixtures/expected/` (chunks y resultados esperados, escritos desde esta tabla).
- El chunker explota patrones estructurales sin IA: ADRs (Contexto/Decisión/Consecuencias), `modules/NN-*/`, `learning/phase-*.md`, units `.service`/`.timer`.
- El scanner **no asume git**: con repo usa `git ls-files`; sin repo, walk + exclusiones explícitas (`.git`, `bin`, `obj`, `node_modules`, `.venv`, `out`, `dist`).
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
