from __future__ import annotations

import os
from pathlib import Path

from typer.testing import CliRunner

from xfds.cli import app

runner: CliRunner = CliRunner()


def test_stops_only_fds_file_in_given_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "one_model"
    assert len(list(directory.iterdir())) == 1

    result = runner.invoke(app, ["stop", str(directory)])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 2


def test_stops_only_fds_file_in_current_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "one_model"
    assert len(list(directory.iterdir())) == 1

    os.chdir(directory)
    result = runner.invoke(app, ["stop"])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 2


def test_stops_specific_fds_file_in_given_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "two_models"
    fds_file = directory / "model1.fds"
    assert len(list(directory.iterdir())) == 2

    result = runner.invoke(app, ["stop", str(fds_file)])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 3


def test_stops_specific_fds_file_in_current_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "two_models"
    assert len(list(directory.iterdir())) == 2

    os.chdir(directory)
    result = runner.invoke(app, ["stop", "model1.fds"])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 3


def test_stops_all_fds_files_in_given_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "two_models"
    assert len(list(directory.iterdir())) == 2

    result = runner.invoke(app, ["-V", "stop", str(directory)])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 4


def test_stops_all_fds_files_in_current_directory(datadir: Path) -> None:
    directory = datadir.resolve() / "two_models"
    assert len(list(directory.iterdir())) == 2

    os.chdir(directory)
    result = runner.invoke(app, ["stop"])

    assert result.exit_code == 0
    assert len(list(directory.iterdir())) == 4
