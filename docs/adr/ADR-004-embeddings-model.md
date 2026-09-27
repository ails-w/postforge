# ADR-004 — Modelo de embeddings local

- **Estado:** aceptado
- **Fecha:** 2026-09-27

## Contexto

El índice (Fases 1-2) necesita recuperación semántica sobre docs en español e inglés, en local, sin servicios externos y sin que el CI descargue modelos. El corpus por proyecto son miles de chunks de documentación y código.

## Spike (2026-09-27)

Script: `scripts/spike_embeddings.py` — 4 consultas en español contra 6 fragmentos reales (focusguard, focusblock, postforge, db-deep-dive), similitud coseno.

| Modelo | Dims | Tiempo total | Hits@1 (doc) | Hits@1 (proyecto) |
|---|---|---|---|---|
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 384 | 13,1 s | 2/4 | **4/4** |
| `minishlab/potion-multilingual-128M` | 256 | 26,4 s | 3/4 | **4/4** |

Notas del spike:

- Los «miss» a nivel documento caen en **otro documento del mismo proyecto** (README vs módulo): el oráculo a nivel doc era ambiguo, no el modelo.
- Los scores son bajos (0,13-0,43): la recuperación semántica sola es ruidosa en fragmentos cortos. **La fusión léxica (FTS5/BM25) es imprescindible** para términos exactos (`pam_time`, `chattr +i`, `AF_UNIX`).
- La descarga de Hugging Face funciona sin token (con warning) y queda cacheada.

## Decisión

- **Default:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384 dims), configurable.
- **Alternativas documentadas:** `potion-multilingual-128M` (más rápido), `mpnet-base` / `multilingual-e5-large` (más calidad; la familia e5 requiere prefijos `query:` / `passage:` — verificar al adoptarla).
- El esquema del índice guarda `model` y `dims`: si cambia el modelo, el índice se reconstruye.
- El CI usa `FakeEmbedder`; los tests reales de embeddings llevan `@pytest.mark.integration` y corren solo en local.

## Consecuencias

**Positivas:**

- Offline, reproducible, multilingüe y sin coste.
- Un solo punto de configuración; cambiar de modelo no toca el pipeline.

**Negativas / coste:**

- Calidad semántica limitada en fragmentos cortos → exige calibrar con el query set del §Oráculo de ingesta y no prescindir del léxico.
- Primera descarga del modelo (~120 MB) en cada máquina nueva; el CI no la hace.

## Referencias

- `scripts/spike_embeddings.py` — medición reproducible.
- `docs/development-plan.md` §Oráculo de ingesta · `docs/adr/ADR-003-rag-per-project-vs-knowledge.md`.
