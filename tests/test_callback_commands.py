"""Integration tests for the `xfds` command."""
from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_version_command() -> None:
    """Test `xfds --version` returns the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.2.0" in result.output
