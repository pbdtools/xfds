"""Integration tests for the `xfds stop` command."""
from pathlib import Path

from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_directory_is_reset_when_requested(fds_file: Path, stop_file: Path) -> None:
    """Test directory is reset when requested."""
    result = runner.invoke(app, ["stop", str(fds_file)])
    assert result.exit_code == 0
    assert stop_file.exists()

    result = runner.invoke(app, ["reset", str(fds_file)])
    assert result.exit_code == 0
    assert len(list(fds_file.parent.iterdir())) == 1
    assert not stop_file.exists()


def test_only_deletes_files_matching_chid(fds_file: Path, stop_file: Path) -> None:
    """Test directory is reset when requested."""
    result = runner.invoke(app, ["stop", str(fds_file)])
    assert result.exit_code == 0
    assert stop_file.exists()

    fds_file.parent.joinpath("pbd.out").touch()
    result = runner.invoke(app, ["reset", "--chid", "pbd", str(fds_file)])
    assert result.exit_code == 0
    assert len(list(fds_file.parent.iterdir())) == 2
    assert stop_file.exists()
