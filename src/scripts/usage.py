"""Update USAGE.md."""
from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()
USAGE_FILE = Path(__file__).parents[2].joinpath("USAGE.md")


def get_help(command: str = "") -> str:
    """Get help text for a command."""
    args = ["--help"]
    if command:
        args.insert(0, command)

    result = runner.invoke(app, args)
    return result.output


def extract_commands(help_text: str) -> list[str]:
    """Extract commands from help text."""
    lines = help_text.splitlines()

    ix = lines.index("Commands:") + 1
    lines = lines[ix:]

    ix = lines.index("")
    lines = lines[:ix]

    return [line.strip().split()[0] for line in lines]


def format_block(command: str | None, help_text: str) -> str:
    """Format help text as a code block."""
    return "\n".join([f"# `xfds {command} --help`", "```", help_text, "```", ""])


def compile_text() -> str:
    """Compile text."""
    commands = extract_commands(get_help())
    commands.insert(0, "")

    usage_text = "\n".join([format_block(cmd, get_help(cmd)) for cmd in commands])
    usage_text = usage_text.replace("Usage: main", "Usage: xfds")

    return usage_text


def generate_usage_file() -> None:
    """Update USAGE.md."""
    USAGE_FILE.write_text(compile_text())


if __name__ == "__main__":
    generate_usage_file()
