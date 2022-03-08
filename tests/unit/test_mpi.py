"""Tests for running in serial vs parallel."""
from __future__ import annotations

import pytest

from xfds import core, mpi


def test_serial_if_processors_is_none(default_cmd_kwargs: dict) -> None:
    """Test container is serial when processors is None."""
    default_cmd_kwargs["processors"] = 1
    cmd = core.build_arguments(**default_cmd_kwargs)
    assert "mpiexec" not in cmd


def test_mpi_if_processors_is_not_none(default_cmd_kwargs: dict) -> None:
    """Test container is mpi when processors is not None."""
    default_cmd_kwargs["processors"] = 2
    cmd = core.build_arguments(**default_cmd_kwargs)
    assert "mpiexec" in cmd


@pytest.mark.parametrize(
    ("fds_records", "n"),
    [
        ("", 0),
        ("&MESH /", 1),
        ("&MESH /\n&MESH /", 2),
        ("&MESH MPI_PROCESS=0/\n&MESH /", 2),
        ("&MESH MPI_PROCESS=0/\n&MESH /\n&MESH MPI_PROCESS=1/", 3),
    ],
)
def test_correct_mpi_proc_count(fds_records: str, n: int) -> None:
    """Test correct number of mpi processes."""
    assert mpi.mpi_process_count(fds_records) == n
