# Handoff — postforge

> Estado MUTABLE. Se sobreescribe al iniciar/cerrar sesión. Última actualización: 2026-09-27.

## Fase activa

**Fase 0 — Setup + research + spikes** (en curso: Lotes 1, 2 y 3 completos — research 4/4 ✅, knowledge completo ✅).

## Próximo paso

1. **Lote 4:** código (`uv`, CLI, `llm.py`, tests, CI) + spikes → ADR-004 (embeddings) y ADR-005 (modelos).
2. **Lote 5:** `prompts/` + learning y progress-log de Fase 0.

## Decisiones recientes

- Stack v1: Python 3.12 + uv; TUI en C# queda como upgrade path → `docs/adr/ADR-001-python-uv-stack.md`.
- LLM vía `opencode run --format json` (suscripción, sin API keys) → `docs/adr/ADR-002-opencode-run-llm-backend.md`.
- RAG por proyecto y `knowledge/` separado del índice → `docs/adr/ADR-003-rag-per-project-vs-knowledge.md`.

## Riesgos

- Wheels para Python 3.14 inexistentes → mitigado: 3.12 gestionado con uv.
- Cuota de la suscripción → mitigado: modelo barato para el map-reduce, fuerte solo para redacción.
- `mmdc` puede requerir Chromium headless → verificar en Fase 4.

## Estado del repo

- Rama `main`; commits directos durante Fase 0.
- Remoto previsto: `https://github.com/ails-w/postforge.git` (repo de GitHub pendiente de crear y primer push).
