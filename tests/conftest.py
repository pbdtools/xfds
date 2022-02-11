"""Tests for command line interface."""
from pathlib import Path

import pytest

from xfds import settings


@pytest.fixture
def latest() -> str:
    """Fixture to point to FDS version."""
    return settings.VERSIONS[-1]


@pytest.fixture
def fds_file(shared_datadir: Path) -> Path:
    """Fixture to point to FDS file."""
    return shared_datadir / "fds" / "test.fds"


@pytest.fixture
def fds_dir(fds_file: Path) -> Path:
    """Fixture to point to FDS directory."""
    return fds_file.parent.resolve()


@pytest.fixture
def empty_dir(shared_datadir: Path) -> Path:
    """Fixture to point to empty directory."""
    return shared_datadir / "no_fds"
