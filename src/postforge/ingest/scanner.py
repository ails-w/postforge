"""Enumerate the files that belong to a project.

One contract, two sources: in a git repository we trust `git ls-files` (the
repo's own `.gitignore` already curated what is content); otherwise we walk
the tree and apply explicit exclusions. Binaries are dropped in both paths.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable
from pathlib import Path

TrackedFiles = Callable[[Path], list[str] | None]

EXCLUDED_DIRS = frozenset({".git", "bin", "obj", "node_modules", ".venv", "venv", "out", "dist"})
SNIFF_BYTES = 8192


def list_tracked_files(root: Path) -> list[str] | None:
    """Return git-tracked paths relative to `root`, or None when there is no git."""
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.splitlines()


def is_binary(path: Path) -> bool:
    """A NUL byte in the first block means binary (git's own heuristic)."""
    try:
        with path.open("rb") as handle:
            return b"\x00" in handle.read(SNIFF_BYTES)
    except OSError:
        return True


def _walk(root: Path) -> list[str]:
    """Non-git fallback: walk the tree, pruning excluded directories."""
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            found.append(path.relative_to(root).as_posix())
    return found


def scan_repo(
    root: Path | str,
    *,
    tracked: TrackedFiles = list_tracked_files,
) -> list[Path]:
    """Project files under `root`, relative and sorted, binaries excluded."""
    base = Path(root)
    candidates = tracked(base)
    if candidates is None:
        candidates = _walk(base)
    return sorted(Path(rel) for rel in candidates if not is_binary(base / rel))
