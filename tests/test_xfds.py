"""Tests for command line interface."""
from pathlib import Path

import pytest

from xfds import settings
from xfds.core import build_arguments

FDS = settings.LATEST


@pytest.fixture
def fds_file(shared_datadir: Path) -> Path:
    """Fixture to point to FDS file."""
    return shared_datadir / "fds" / "test.fds"


@pytest.fixture
def empty_dir(shared_datadir: Path) -> Path:
    """Fixture to point to empty directory."""
    return shared_datadir / "no_fds"


def test_command_with_default_arguments(fds_file: Path) -> None:
    """Test command with default arguments."""
    volume = fds_file.parent.resolve()

    given = build_arguments(fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:/workdir "
        f"openbcl/fds:{FDS} fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_with_default_interactive_mode() -> None:
    """Test command with default interactive mode."""
    volume = Path.cwd().resolve()

    given = build_arguments(interactive=True)
    expected = (
        f"docker run --rm -it --name fds-{FDS} -v {volume}:/workdir "
        f"openbcl/fds:{FDS}"
    )
    assert " ".join(given) == expected


def test_command_for_linux_container(fds_file: Path) -> None:
    """Test command for linux container."""
    volume = fds_file.parent.resolve()

    given = build_arguments(fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:/workdir "
        f"openbcl/fds:{FDS} fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_for_windows_container(fds_file: Path) -> None:
    """Test command for windows container."""
    volume = fds_file.parent.resolve()

    given = build_arguments(windows=True, fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:C:\\workdir "
        f"openbcl/fds:{FDS} fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_for_linux_mpi(fds_file: Path) -> None:
    """Test command for linux mpi."""
    processors = 2
    volume = fds_file.parent.resolve()

    given = build_arguments(processors=processors, fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:/workdir "
        f"openbcl/fds:{FDS} mpiexec -n {processors} fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_for_windows_mpi(fds_file: Path) -> None:
    """Test command for windows mpi."""
    processors = 2
    volume = fds_file.parent.resolve()

    given = build_arguments(windows=True, processors=processors, fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:C:\\workdir "
        f"openbcl/fds:{FDS} mpiexec -n {processors} fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_for_linux_interactive() -> None:
    """Test command for linux interactive."""
    volume = Path.cwd().resolve()

    given = build_arguments(interactive=True)
    expected = (
        f"docker run --rm -it --name fds-{FDS} -v {volume}:/workdir "
        f"openbcl/fds:{FDS}"
    )
    assert " ".join(given) == expected


def test_command_for_windows_interactive() -> None:
    """Test command for windows interactive."""
    volume = Path.cwd().resolve()

    given = build_arguments(windows=True, interactive=True)
    expected = (
        f"docker run --rm -it --name fds-{FDS} -v {volume}:C:\\workdir "
        f"openbcl/fds:{FDS}"
    )
    assert " ".join(given) == expected


def test_command_with_custom_version(fds_file: Path) -> None:
    """Test command with custom version."""
    volume = fds_file.parent.resolve()

    given = build_arguments(version="6.2.0", fds_file=fds_file)
    expected = (
        f"docker run --rm --name {fds_file.stem} -v {volume}:/workdir "
        f"openbcl/fds:6.2.0 fds {fds_file.name}"
    )
    assert " ".join(given) == expected


def test_command_when_interactive_and_file_specified(fds_file: Path) -> None:
    """Test command when interactive and file specified."""
    given = build_arguments(interactive=True, fds_file=fds_file)
    expected = (
        f"docker run --rm -it --name fds-{FDS} -v {Path.cwd().resolve()}:/workdir "
        f"openbcl/fds:{FDS}"
    )
    assert " ".join(given) == expected


def test_finds_fds_file_when_directory_is_specified(fds_file: Path) -> None:
    """Test finds fds file when directory is specified."""
    given = build_arguments(fds_file=fds_file.parent)
    expected = (
        f"docker run --rm --name test -v {fds_file.parent.resolve()}:/workdir "
        f"openbcl/fds:{FDS} fds test.fds"
    )
    assert " ".join(given) == expected


def test_enters_interactive_mode_if_no_fds_file_in_directory(empty_dir: Path) -> None:
    """Test enters interactive mode if no fds file in directory."""
    given = build_arguments(fds_file=empty_dir)
    expected = (
        f"docker run --rm -it --name fds-{FDS} -v {empty_dir.resolve()}:/workdir "
        f"openbcl/fds:{FDS}"
    )
    assert " ".join(given) == expected
