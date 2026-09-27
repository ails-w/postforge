"""postforge command-line interface.

Phase 0 registers the final command surface as stubs: `--help` lists every
command, and each stub reports the phase that will implement it.
"""

import typer
from rich.console import Console

from postforge import __version__

app = typer.Typer(
    name="postforge",
    help="Generate LinkedIn posts and project-form fields from a repository's real documentation.",
    no_args_is_help=False,
    add_completion=False,
)
console = Console()


def _not_implemented(command: str, phase: int) -> None:
    console.print(f"[yellow]{command}[/yellow] is not implemented yet (phase {phase}).")
    raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    if version:
        console.print(f"postforge {__version__}")
        raise typer.Exit(code=0)
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit(code=0)


@app.command()
def index(slug: str) -> None:
    """Scan a project and build its search index (phase 1)."""
    _not_implemented("index", 1)


@app.command()
def brief(slug: str) -> None:
    """Distill the indexed project into brief.json with cited evidence (phase 2)."""
    _not_implemented("brief", 2)


@app.command()
def gen(slug: str) -> None:
    """Generate post variants, form fields and checklist (phase 3)."""
    _not_implemented("gen", 3)


@app.command()
def refine(slug: str) -> None:
    """Iterate on a generated post in a chat session (phase 3)."""
    _not_implemented("refine", 3)


@app.command()
def visuals(slug: str) -> None:
    """Render diagrams, snippets, GIFs and covers into media/ (phase 4)."""
    _not_implemented("visuals", 4)


def main() -> None:
    app()
