"""Tests for running in serial vs parallel."""
from __future__ import annotations

from xfds._run import build_arguments


def test_serial_if_processors_is_none(default_cmd_kwargs: dict) -> None:
    """Test container is serial when processors is None."""
    default_cmd_kwargs["processors"] = 1
    cmd = build_arguments(**default_cmd_kwargs)
    assert "mpiexec" not in cmd


def test_mpi_if_processors_is_not_none(default_cmd_kwargs: dict) -> None:
    """Test container is mpi when processors is not None."""
    default_cmd_kwargs["processors"] = 2
    cmd = build_arguments(**default_cmd_kwargs)
    assert "mpiexec" in cmd
