"""Integration tests for the `xfds pbs` command."""
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


@pytest.fixture
def pbs_file(fds_file: Path) -> Generator[Path, None, None]:
    """Create a pbs file."""
    pbs_file = fds_file.with_suffix(".pbs")
    if pbs_file.exists():
        pbs_file.unlink()

    assert not pbs_file.exists()
    yield pbs_file


def test_versions_command(fds_file: Path, pbs_file: Path) -> None:
    """Test versions command displays list of fds versions."""
    result = runner.invoke(app, ["pbs", str(fds_file)])
    assert result.exit_code == 0
    assert pbs_file.exists()
