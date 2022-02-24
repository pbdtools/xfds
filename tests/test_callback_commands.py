"""Integration tests for the `xfds` command."""
from typer.testing import CliRunner

from xfds import __version__
from xfds.cli import app

runner = CliRunner()


def test_version_command() -> None:
    """Test `xfds --version` returns the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output