# ADR-005 — Modelos del pipeline y contrato JSON de `opencode run`

- **Estado:** aceptado
- **Fecha:** 2026-09-27

## Contexto

El pipeline hace tres llamadas al LLM (extraer hechos, sintetizar brief, redactar y criticar) y `refine` abre una cuarta vía conversacional. Hay que fijar los tiers, los modelos y el contrato exacto de invocación.

## Spike (2026-09-27), contrato observado con opencode v2.0.14

```text
opencode run -m <provider/model> --format json "<prompt>"
```

emite **JSONL de eventos**, uno por línea:

```json
{"type":"text","sessionID":"ses_…","part":{"type":"text","text":"ok","time":{…}}}
```

- El texto vive en `part.text` de los eventos `type=text`.
- `sessionID` aparece en todos los eventos y se reutiliza con `--session`: esa es la base de `refine`.
- Éxito: exit code 0 y stderr vacío. Smoke test real del adaptador: OK (`adapter ok` + sesión devuelta).
- Implementado en `src/postforge/llm.py` (`parse_events`, `OpenCodeLlm`) con tests unitarios.

## Precios (USD por millón de tokens, opencode-go, 2026-09-27)

| Tier | Modelo | Entrada | Salida | Cache read |
|---|---|---|---|---|
| Map barato | `opencode-go/deepseek-v4.1-flash` | 0,15 | 0,60 | 0,003 |
| Redacción fuerte | `opencode-go/glm-5.3` | 1,40 | 4,40 | 0,26 |
| Smoke gratis | `opencode-go/longcat-2.5-preview-free` | 0 | 0 | 0 |

Alternativas: `deepseek-v4-pro` (0,66/1,98, tier medio) · `kimi-k3` (3/15, premium).

## Decisión

- `model_fast` (map/reduce): `opencode-go/deepseek-v4.1-flash`.
- `model_write` (post, critique, refine): `opencode-go/glm-5.3`.
- Todo configurable (config del proyecto + env + `--model` por corrida).
- **Coste estimado de una corrida completa: < USD 0,02** (map de ~30 chunks con flash + una redacción con glm).

## Consecuencias

**Positivas:**

- Un solo lugar que tocar si OpenCode cambia el formato: `llm.py`.
- `refine` reutiliza el `sessionID` → chat con el contexto del brief ya cargado.
- Los tests de CI nunca invocan el LLM (usan `FakeLlm`).

**Negativas / coste:**

- Acoplamiento al CLI de OpenCode (mitigado por el adaptador y `--standalone` para aislar problemas).
- El consumo afecta la cuota de la suscripción; mitigado con el tier barato para el map.

## Referencias

- `src/postforge/llm.py` · `tests/test_llm.py` · `docs/architecture.md` §Contrato con el LLM.
