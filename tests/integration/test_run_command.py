"""Integration tests for the `xfds run` command."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Generator

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
    pbs_file.unlink()


def timeout(
    callback: Callable, timeout: float = 30.0, interval: float = 0.1, *args
) -> None:
    """Timeout function."""
    start = time.time()
    while not callback(*args) and time.time() - start < timeout:
        time.sleep(interval)


def unlink(file: Path) -> None:
    """Unlink file."""
    try:
        file.unlink()
    except FileNotFoundError:
        pass


def test_run_command_with_fds_file(fds_file: Path) -> None:
    """Test run command with fds file."""
    result = runner.invoke(app, ["--dry-run", "run", str(fds_file)])
    assert result.exit_code == 0
    assert "openbcl/fds:latest bash -c fds test.fds" in result.output.replace("\n", "")


def test_run_command_with_fds_file_and_interactive(fds_file: Path) -> None:
    """Test run command with fds file."""
    result = runner.invoke(app, ["--dry-run", "run", "-i", str(fds_file)])
    assert result.exit_code == 0
    assert "-it" in result.output
    assert "fds test.fds" not in result.output


def test_run_command_executes_fds(fds_file: Path) -> None:
    """Test run command executes fds."""
    out_file = fds_file.with_suffix(".out")
    unlink(out_file)
    assert out_file.exists() is False

    result = runner.invoke(app, ["run", str(fds_file)])
    assert result.exit_code == 0

    timeout(out_file.exists)
    assert out_file.exists() is True
