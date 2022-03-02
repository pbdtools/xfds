"""Integration tests for the `xfds stop` command."""
from pathlib import Path

from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_creates_stop_file_when_requested(fds_file: Path, stop_file: Path) -> None:
    """Test creates stop file when requested."""
    result = runner.invoke(app, ["stop", str(fds_file)])
    assert result.exit_code == 0
    assert stop_file.exists()
