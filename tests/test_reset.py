"""Integration tests for the `xfds stop` command."""
from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_reset_directory(datadir: Path) -> None:
    directory = datadir / "model" / "output" / "model_0.10"
    n_starting_files = len(list(directory.iterdir()))

    result = runner.invoke(app, ["reset", str(directory)])
    assert result.exit_code == 0

    n_files = len(list(directory.iterdir()))
    assert n_starting_files != n_files


def test_no_effect_after_reset(datadir: Path) -> None:
    directory = datadir / "model" / "output" / "model_0.15"
    n_starting_files = len(list(directory.iterdir()))

    result = runner.invoke(app, ["reset", str(directory)])
    assert result.exit_code == 0

    n_files = len(list(directory.iterdir()))
    assert n_starting_files == n_files
