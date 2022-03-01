"""Integration tests for the `xfds run` command."""
from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_versions_command() -> None:
    """Test versions command displays list of fds versions."""
    result = runner.invoke(app, ["versions"])
    assert result.exit_code == 0
    assert "latest" not in result.output
    assert len(result.output.splitlines()) >= 3
