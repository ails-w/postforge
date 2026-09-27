"""Adapter around `opencode run` — the only place postforge talks to an LLM.

Contract observed in the phase 0 spike (2026-09-27, opencode v2.0.14):

    opencode run -m <provider/model> --format json "<prompt>"

emits newline-delimited JSON events; text arrives in `part.text` of events
whose `type` is "text", and every event carries a `sessionID` that can be
reused later with `--session` (the `refine` command builds on this).
"""

import json
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


class LlmError(RuntimeError):
    """Raised when the LLM call fails or its output breaks the contract."""


@dataclass(frozen=True)
class LlmResult:
    text: str
    session_id: str | None = None
    model: str | None = None


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class CommandRunner(Protocol):
    """Seam for tests: anything that can run an argv and capture its output."""

    def run(self, argv: Sequence[str]) -> CommandResult: ...


class LlmClient(Protocol):
    """Seam for the pipeline: anything that can turn a prompt into text."""

    def complete(self, prompt: str, *, model: str, session_id: str | None = None) -> LlmResult: ...


class SubprocessRunner:
    """Real runner. Only used outside unit tests."""

    def run(self, argv: Sequence[str]) -> CommandResult:
        completed = subprocess.run(list(argv), capture_output=True, text=True)
        return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def parse_events(stdout: str) -> LlmResult:
    """Parse the JSONL event stream emitted by `opencode run --format json`."""
    texts: list[str] = []
    session_id: str | None = None

    for number, raw in enumerate(stdout.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise LlmError(f"invalid JSON on line {number}: {line[:120]}") from error
        if not isinstance(event, dict):
            raise LlmError(f"unexpected event on line {number}: {line[:120]}")

        session_id = event.get("sessionID") or session_id
        if event.get("type") == "text":
            part = event.get("part") or {}
            text = part.get("text")
            if isinstance(text, str):
                texts.append(text)

    if not texts:
        raise LlmError("no text events in response")
    return LlmResult(text="".join(texts), session_id=session_id)


class OpenCodeLlm:
    """`LlmClient` backed by the user's OpenCode subscription (no API keys)."""

    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner or SubprocessRunner()

    def complete(self, prompt: str, *, model: str, session_id: str | None = None) -> LlmResult:
        argv = ["opencode", "run", "-m", model, "--format", "json"]
        if session_id:
            argv += ["--session", session_id]
        argv.append(prompt)

        result = self._runner.run(argv)
        if result.returncode != 0:
            tail = (result.stderr or result.stdout).strip()[-500:]
            raise LlmError(f"opencode run failed ({result.returncode}): {tail}")

        parsed = parse_events(result.stdout)
        return LlmResult(text=parsed.text, session_id=parsed.session_id, model=model)
