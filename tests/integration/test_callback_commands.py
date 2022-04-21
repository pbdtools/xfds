"""Integration tests for the `xfds` command."""
from __future__ import annotations

from typer.testing import CliRunner

from xfds import __version__
from xfds.cli import app

runner: CliRunner = CliRunner()


def test_version_command() -> None:
    """Test `xfds --version` returns the correct version."""
    runner.invoke(app)
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


if __name__ == "__main__":
    test_version_command()
