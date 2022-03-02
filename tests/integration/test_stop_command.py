"""Integration tests for the `xfds stop` command."""
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


@pytest.fixture
def stop_file(fds_file: Path) -> Generator[Path, None, None]:
    """Create a stop file."""
    _stop_file = fds_file.with_suffix(".stop")
    if _stop_file.exists():
        _stop_file.unlink()

    assert not _stop_file.exists()
    yield _stop_file
    _stop_file.unlink()


def test_creates_stop_file_when_requested(fds_file: Path, stop_file: Path) -> None:
    """Test creates stop file when requested."""
    result = runner.invoke(app, ["stop", str(fds_file)])
    assert result.exit_code == 0
    assert stop_file.exists()
