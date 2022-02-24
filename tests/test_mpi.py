"""Tests for running in serial vs parallel."""
from __future__ import annotations

from pathlib import Path

import pytest

from xfds import core


@pytest.fixture
def kwargs(fds_file: Path) -> dict:
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
        container_name=_container,
    )


def test_serial_if_processors_is_none(kwargs: dict) -> None:
    """Test container is serial when processors is None."""
    cmd = core.build_arguments(processors=1, **kwargs)
    assert "mpiexec" not in cmd


def test_mpi_if_processors_is_not_none(kwargs: dict) -> None:
    """Test container is mpi when processors is not None."""
    cmd = core.build_arguments(processors=2, **kwargs)
    assert "mpiexec" in cmd
