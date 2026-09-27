from typer.testing import CliRunner

from postforge import __version__
from postforge.cli import app

runner = CliRunner()


def test_cli_help_exits_zero_and_lists_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    for command in ("index", "brief", "gen", "refine", "visuals"):
        assert command in result.output


def test_cli_without_args_shows_help_and_exits_zero() -> None:
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Usage" in result.output


def test_cli_version_flag_prints_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_stub_exits_one_and_names_its_phase() -> None:
    result = runner.invoke(app, ["index", "focusguard"])

    assert result.exit_code == 1
    assert "phase 1" in result.output.lower()


def test_cli_every_stub_points_to_a_phase() -> None:
    for command, phase in (
        ("brief", "phase 2"),
        ("gen", "phase 3"),
        ("refine", "phase 3"),
        ("visuals", "phase 4"),
    ):
        result = runner.invoke(app, [command, "focusguard"])
        assert result.exit_code == 1
        assert phase in result.output.lower()
