import json

import pytest

from postforge.llm import (
    CommandResult,
    LlmError,
    OpenCodeLlm,
    parse_events,
)

SESSION_ID = "ses_f1d48e70effe7aqu2FVmbvBpA1"


def text_event(text: str, session_id: str = SESSION_ID) -> str:
    payload = {
        "type": "text",
        "timestamp": 1790510049719,
        "sessionID": session_id,
        "part": {
            "id": "prt_0e2b71a2d001mkecWvVMDJtrMa_text-0",
            "sessionID": session_id,
            "messageID": "msg_0e2b71a2d001mkecWvVMDJtrMa",
            "type": "text",
            "text": text,
            "time": {"start": 1790510045761, "end": 1790510049719},
        },
    }
    return json.dumps(payload)


def test_parse_events_returns_text_and_session_id() -> None:
    result = parse_events(text_event("ok") + "\n")

    assert result.text == "ok"
    assert result.session_id == SESSION_ID


def test_parse_events_concatenates_multiple_text_events() -> None:
    stdout = text_event("part one ") + "\n" + text_event("part two") + "\n"

    result = parse_events(stdout)

    assert result.text == "part one part two"


def test_parse_events_ignores_blank_lines() -> None:
    result = parse_events("\n" + text_event("ok") + "\n\n")

    assert result.text == "ok"


def test_parse_events_raises_on_malformed_line() -> None:
    with pytest.raises(LlmError, match="invalid JSON"):
        parse_events("not-json\n")


def test_parse_events_raises_when_no_text_events() -> None:
    non_text = json.dumps({"type": "step_start", "sessionID": SESSION_ID})

    with pytest.raises(LlmError, match="no text events"):
        parse_events(non_text + "\n")


class FakeRunner:
    def __init__(self, result: CommandResult) -> None:
        self.result = result
        self.argv: list[str] | None = None

    def run(self, argv: list[str]) -> CommandResult:
        self.argv = list(argv)
        return self.result


def test_client_builds_opencode_run_command() -> None:
    runner = FakeRunner(CommandResult(0, text_event("ok") + "\n", ""))
    client = OpenCodeLlm(runner=runner)

    client.complete("Write a post", model="opencode-go/test-model")

    assert runner.argv == [
        "opencode",
        "run",
        "-m",
        "opencode-go/test-model",
        "--format",
        "json",
        "Write a post",
    ]


def test_client_passes_session_when_given() -> None:
    runner = FakeRunner(CommandResult(0, text_event("ok") + "\n", ""))
    client = OpenCodeLlm(runner=runner)

    client.complete("Refine it", model="opencode-go/test-model", session_id=SESSION_ID)

    assert runner.argv is not None
    assert "--session" in runner.argv
    assert runner.argv[runner.argv.index("--session") + 1] == SESSION_ID


def test_client_returns_result_on_success() -> None:
    runner = FakeRunner(CommandResult(0, text_event("hello") + "\n", ""))
    client = OpenCodeLlm(runner=runner)

    result = client.complete("hi", model="opencode-go/test-model")

    assert result.text == "hello"
    assert result.session_id == SESSION_ID
    assert result.model == "opencode-go/test-model"


def test_client_raises_on_nonzero_exit_with_stderr_tail() -> None:
    runner = FakeRunner(CommandResult(2, "", "boom: model not found"))
    client = OpenCodeLlm(runner=runner)

    with pytest.raises(LlmError, match="boom: model not found"):
        client.complete("hi", model="opencode-go/missing")


def test_client_raises_when_stdout_has_no_payload() -> None:
    runner = FakeRunner(CommandResult(0, "", ""))
    client = OpenCodeLlm(runner=runner)

    with pytest.raises(LlmError, match="no text events"):
        client.complete("hi", model="opencode-go/test-model")
