# ADRs — postforge

Registro de decisiones de arquitectura. **Una decisión = un archivo**, y cada ADR refleja la decisión **vigente** (si cambia, se actualiza o se reemplaza con otro ADR).

| ADR | Decisión | Estado |
|---|---|---|
| [ADR-001](ADR-001-python-uv-stack.md) | Python 3.12 + uv como stack de la v1 | ✅ aceptado |
| [ADR-002](ADR-002-opencode-run-llm-backend.md) | `opencode run --format json` como backend LLM | ✅ aceptado |
| [ADR-003](ADR-003-rag-per-project-vs-knowledge.md) | RAG por proyecto y `knowledge/` como capa separada | ✅ aceptado |
| [ADR-004](ADR-004-embeddings-model.md) | Modelo de embeddings local | ✅ aceptado |
| [ADR-005](ADR-005-models-and-json-contract.md) | Modelos del pipeline y contrato JSON de `opencode run` | ✅ aceptado |

## Cuándo crear un ADR

- Cuando se elige entre alternativas con trade-offs reales.
- Cuando la decisión es costosa de revertir.
- Cuando alguien futuro va a preguntar "¿por qué está hecho así?".

No hace falta ADR para detalles reversibles de implementación.

## Plantilla

Usar `template-adr.md`. Convención de nombre: `ADR-0NN-titulo-corto.md`.
