# Handoff — postforge

> Estado MUTABLE. Se sobreescribe al iniciar/cerrar sesión. Última actualización: 2026-09-27.

## Fase activa

**Fase 0 — Setup + research + spikes** (en curso: Lotes 1, 2, 3 y 4 completos; **solo falta el Lote 5**: prompts + learning/progress-log de Fase 0).

## Próximo paso

1. **Lote 5:** `prompts/` (extract-facts, synthesize-brief, write-post, critique-post) + `phase-00-setup.md` y `progress-log/phase-00-setup.md` → cierra Fase 0.
2. Después: Fase 1 (ingesta + índice) en rama `dev` con PR al cerrar.

## Decisiones recientes

- Stack v1: Python 3.12 + uv (ADR-001). TUI en C# como upgrade path.
- LLM vía `opencode run --format json` (ADR-002); contrato JSONL + `sessionID` verificado (ADR-005).
- RAG por proyecto y `knowledge/` separado (ADR-003).
- Embeddings: `paraphrase-multilingual-MiniLM-L12-v2` por defecto (ADR-004).
- Modelos: `deepseek-v4.1-flash` (map) + `glm-5.3` (redacción); corrida completa < USD 0,02 (ADR-005).
- Interacción: batch + `refine` (chat que reusa `sessionID`).

## Estado del código (Lote 4)

- `uv sync` funcionando con Python 3.12.14 gestionado por uv; `uv.lock` commiteado.
- CLI con 5 comandos como stubs (`--help`, `--version`); 15 tests en verde; ruff limpio.
- `llm.py`: adaptador real probado contra la suscripción (`adapter ok` + sesión devuelta).
- CI configurado (setup-uv v10.1.0 + `uv sync --frozen` + ruff + pytest); **sin verificar hasta el primer push**.
- Spike de embeddings corrido: `scripts/spike_embeddings.py` (4/4 proyecto correcto en ambos modelos).
- Guía nueva: `docs/learning/uv.md` (concepto transversal).

## Riesgos

- CI sin verificar: el primer push de GitHub es la prueba real (letra chica: `enable-cache` + lock).
- Wheels para Python 3.14 inexistentes → mitigado: 3.12 gestionado con uv.
- Cuota de la suscripción → mitigado: tier barato para el map; modelos configurables.
- `mmdc` puede requerir Chromium headless → verificar en Fase 4.
- Secretos: nada de la auth de OpenCode entra al repo (ver `docs/architecture.md` §Datos que NUNCA entran al repo). Opcional: `gitleaks` como pre-commit antes del push público.

## Estado del repo

- Rama `main`; commits directos durante Fase 0. Al iniciar Fase 1: rama `dev` + PR al cerrar fase.
- Remoto previsto: `https://github.com/ails-w/postforge.git` (repo de GitHub pendiente de crear y primer push).
