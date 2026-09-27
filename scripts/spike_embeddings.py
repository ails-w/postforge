"""Spike (phase 0): rank real project snippets against Spanish queries.

Usage:
    uv run --with fastembed python scripts/spike_embeddings.py --model <model>

This is a one-off measurement, not part of the package: the phase 2 index will
absorb whatever wins here (see docs/adr/ADR-004-embeddings-model.md).
"""

import argparse
import pathlib
import time

QUERIES = [
    "¿cómo evito que alguien entre fuera del horario permitido?",
    "el display manager quedó en pantalla negra tras matar la sesión",
    "¿cómo se comunican la TUI y el daemon sin red?",
    "fricción deliberada antes de detener el bloqueo",
]

DOCS = [
    ("focusguard/README.md", "Projects/focusguard/README.md"),
    ("focusguard/01-pam-gate", "Projects/focusguard/modules/01-pam-gate/README.md"),
    ("focusblock/ADR-002-ipc", "Projects/focusblock/docs/adr/ADR-002-ipc-unix-socket.md"),
    ("focusblock/phase-04", "Projects/focusblock/docs/learning/phase-04-blocker.md"),
    ("postforge/README.md", "Projects/postforge/README.md"),
    ("db-deep-dive/README.md", "Projects/db-deep-dive-portfolio/README.md"),
]

EXPECTED = {0: "focusguard/01-pam-gate", 1: "focusguard/README.md", 2: "focusblock/ADR-002-ipc", 3: "focusblock/phase-04"}


def read_snippet(relative: str, limit: int = 900) -> str:
    path = pathlib.Path.home() / relative
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:limit]


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot / (norm_a * norm_b)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    from fastembed import TextEmbedding

    labels = [label for label, _ in DOCS]
    documents = [f"{label}\n{read_snippet(path)}" for label, path in DOCS]

    started = time.monotonic()
    model = TextEmbedding(model_name=args.model)
    doc_vectors = list(model.embed(documents))
    query_vectors = list(model.embed(QUERIES))
    elapsed = time.monotonic() - started

    print(f"model: {args.model} ({len(doc_vectors[0])} dims, {elapsed:.1f}s total)")
    hits_at_1 = 0
    for index, (query, vector) in enumerate(zip(QUERIES, query_vectors)):
        scores = sorted(
            ((cosine(vector, doc), label) for doc, label in zip(doc_vectors, labels)),
            reverse=True,
        )
        top = ", ".join(f"{label} ({score:.3f})" for score, label in scores[:2])
        hit = scores[0][1] == EXPECTED[index]
        hits_at_1 += hit
        print(f"[{'HIT' if hit else 'MISS'}] {query}\n        top-2: {top}")

    print(f"\nhits@1: {hits_at_1}/{len(QUERIES)}")


if __name__ == "__main__":
    main()
