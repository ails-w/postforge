# ADR-002 — `opencode run --format json` como backend LLM

- **Estado:** aceptado
- **Fecha:** 2026-09-26

## Contexto

El generador necesita un LLM potente sin gestionar claves de API. El autor ya paga la suscripción de OpenCode y el CLI está autenticado en la máquina (`opencode v2`, 41 modelos disponibles). Además, la publicación en LinkedIn debe ser manual (no hay API para el perfil personal), así que el LLM solo se usa para **analizar y redactar**.

## Decisión

El LLM se invoca como subproceso:

```text
opencode run -m <provider/model> --format json "<prompt>"
```

a través del adaptador `llm.py`. La salida JSON se valida con Pydantic antes de usarse. El pipeline usa **dos tiers**: un modelo barato para el map-reduce y uno fuerte para la redacción final (decisión de modelos → ADR-005).

## Alternativas consideradas

| Alternativa | Por qué no |
|---|---|
| SDK/API directa de un proveedor | Requiere claves y facturación aparte; la suscripción ya cubre el uso |
| Modelo local (Ollama) | No hay GPU ni Ollama instalados; la calidad de redacción importa más que el coste cero |
| Automatizar el navegador para publicar | Viola los términos de uso y arriesga la cuenta; descartado por diseño |

## Consecuencias

**Positivas:**

- Cero gestión de credenciales: el CLI ya está autenticado.
- Cambiar de modelo es cambiar un flag; el adaptador aísla el resto del código.
- Los tests unitarios usan `FakeLlm`; el CI nunca depende del servicio.

**Negativas / coste:**

- Dependencia del servicio de OpenCode y de su CLI (`--standalone` existe para aislar problemas).
- El consumo afecta la cuota de la suscripción: se mitiga con el tier barato para el map.

## Referencias

- `docs/architecture.md` — contrato con el LLM.
- `docs/development-plan.md` — seam `LlmClient` y `FakeLlm`.
