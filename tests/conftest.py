"""Tests for command line interface."""
from pathlib import Path
from typing import Generator

import pytest

from xfds import core


@pytest.fixture
def xfds_datadir() -> Path:
    """Return the path to the xfds data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def latest() -> str:
    """Fixture to point to FDS version."""
    return "6.7.7"


@pytest.fixture
def fds_file(xfds_datadir: Path) -> Path:
    """Fixture to point to FDS file."""
    return xfds_datadir / "fds" / "test.fds"


@pytest.fixture
def stop_file(fds_file: Path) -> Generator[Path, None, None]:
    """Create a stop file."""
    _stop_file = fds_file.with_suffix(".stop")
    if _stop_file.exists():
        _stop_file.unlink()

    assert not _stop_file.exists()
    yield _stop_file
    if _stop_file.exists():
        _stop_file.unlink()


@pytest.fixture
def fds_dir(fds_file: Path) -> Path:
    """Fixture to point to FDS directory."""
    return fds_file.parent.resolve()


@pytest.fixture
def empty_dir(xfds_datadir: Path) -> Path:
    """Fixture to point to empty directory."""
    return xfds_datadir / "no_fds"


@pytest.fixture
def meta_dir(xfds_datadir: Path) -> Path:
    """Fixture to point to empty directory."""
    return xfds_datadir / "from_metadata"


@pytest.fixture
def default_cmd_kwargs(fds_file: Path) -> dict:
    """Build the command line arguments for the CLI."""
    _interactive = False
    _version = "latest"
    _volume = core.volume_to_mount(fds_file=fds_file)
    _container = core.container_name(
        fds_file=fds_file, version=_version, interactive=_interactive
    )

    return dict(
        fds_file=fds_file,
        volume=_volume,
        interactive=_interactive,
        version=_version,
        container=_container,
        processors=1,
    )
