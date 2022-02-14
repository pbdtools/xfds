"""Tests for running in serial vs parallel."""
from pathlib import Path

from xfds.core import build_arguments


def test_serial_if_processors_is_none(fds_file: Path) -> None:
    """Test container is serial when processors is None."""
    cmd = build_arguments(processors=1, fds_file=fds_file)
    assert "mpiexec" not in cmd


def test_mpi_if_processors_is_not_none(fds_file: Path) -> None:
    """Test container is mpi when processors is not None."""
    cmd = build_arguments(processors=2, fds_file=fds_file)
    assert "mpiexec" in cmd
