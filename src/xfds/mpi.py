"""Functions for determining the number of cores required for a FDS simulation."""
from __future__ import annotations

import re
from typing import Optional


def _get_mpi_process(text: str) -> Optional[int]:
    """Extracts the MPI process from a text string."""
    matches = re.search(r"MPI_PROCESS\s*=\s*(\d+)", text)
    if matches is None:
        return None
    return int(matches.group(1))


def _extract_meshes(text: str) -> list[str]:
    """Extract &MESH records from a text string."""
    matches = re.findall(r"&MESH[^/]*/", text)
    if matches is None:
        return []
    return matches


def mpi_process_count(fds_text: str) -> int:
    """Determine how many cores are required for a FDS simulation.

    MPI_PROCESS must be continuous and monotonically increasing.
    If MPI_PROCESS is not specified, it is assumed that the MESH should
    have its own process.
    """
    processes = [_get_mpi_process(record) for record in _extract_meshes(fds_text)]

    implicit = [p for p in processes if p is None]
    explicit = set([p for p in processes if p is not None])

    return len(explicit) + len(implicit)
