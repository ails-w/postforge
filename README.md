# postforge

> Generate LinkedIn posts and project-form fields from a repository's real documentation.

`postforge` scans a local project, builds a per-project RAG index (SQLite FTS5 +
local embeddings), distills a small evidence brief, and writes a ready-to-paste LinkedIn
post plus the fields for LinkedIn's "Add project" form.

**Status:** Phase 0 — the CLI and the LLM adapter already run; index, brief, write and visuals land in phases 1-4.

## Quickstart

```bash
uv sync
uv run postforge --help
```

## Problem

Writing a good project post for LinkedIn is slow and easy to get wrong: recruiters search
by keywords and skills, the feed truncates early, and dumping a whole repository into an
LLM produces generic text. postforge fixes this with evidence:

1. **Ingest** — scan the repository (docs, ADRs, code) and chunk it.
2. **Index** — SQLite FTS5 + local embeddings, one index per project.
3. **Understand** — map-reduce the evidence into `brief.json` (stack, problem, metrics).
4. **Write** — render post variants and form fields using curated editorial rules.
5. **Visuals** — Mermaid diagrams to PNG, terminal GIFs, code shots, cover image.

## Stack and why

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.12 (uv) | RAG ecosystem; fastest path to a working CLI |
| Index | SQLite FTS5 + sqlite-vec | One file, no services, lexical + vector hybrid |
| Embeddings | fastembed (ONNX) | Local, light, multilingual (ES/EN docs) |
| LLM | `opencode run` | Uses the user's OpenCode subscription; no API keys |
| Templates | Jinja2 | Editorial rules separated from code |

## Documentation

Start at [`docs/index.md`](docs/index.md).

## License

MIT
