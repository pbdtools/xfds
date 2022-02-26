"""Functions for creating a .pbs script for Portable Batch System (PBS)."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent


def _clusters(processors: int) -> str:
    """Return the clusters for PBS job scheduler."""
    return f"#PBS -l nodes=1:ppn={processors}"


def _name(fds_file: Path) -> str:
    """Return the name of the .pbs script."""
    if fds_file is None:
        raise TypeError("fds_file must be specified.")
    if not fds_file.is_file():
        raise TypeError(f"{fds_file} is not a file.")
    return f"#PBS -N {fds_file.stem}"


def _email(emails: list[str] = None) -> str:
    """Return an email address for PBS job scheduler."""
    if emails:
        return f"#PBS -m abe\n#PBS -M {';'.join(emails)}"
    return ""


def _shell(shell: str = None) -> str:
    """Return the shell for PBS."""
    _shell = shell or "/bin/bash"
    return f"#PBS -S {_shell}"


def _max_time(max_time: float = 0) -> str:
    """Return the maximum time for PBS job scheduler."""
    if max_time <= 0:
        return ""

    h = max_time
    m = 60 * (h % 1)
    s = 60 * (m % 1)
    h, m, s = int(h), int(m), int(s)
    return f"#PBS -l walltime={h:d}:{m:02d}:{s:02d}"


def _module_load(version: str) -> str:
    """Return the load modules for PBS job scheduler."""
    if version is None:
        raise TypeError("version must be specified.")

    text = dedent(
        """
    # load required modules
    module load fds
    """.rstrip()
    )
    if version not in ["", "latest"]:
        text += f"/{version}"

    return text


def _setup() -> str:
    """Return the setup for PBS job scheduler."""
    return dedent(
        """
    # change to the working directory
    cd $PBS_O_WORKDIR

    # set MPI variables
    export I_MPI_PIN=1
    export I_MPI_PIN_MODE=pm
    export OMP_NUM_THREADS=1
    export MPI_PPN=$(($PBS_NUM_PPN / $OMP_NUM_THREADS))
    export MPI_NP=$(($PBS_NP / $OMP_NUM_THREADS))
    """.rstrip()
    )


def _commands(fds_file: Path) -> str:
    """Return the commands for PBS job scheduler."""
    return dedent(
        f"""
    # run fds in parallel
    mpiexec -np $MPI_NP fds_mpi {fds_file.name}
    """.rstrip()
    )


def generate_pbs(
    fds_file: Path,
    version: str,
    processors: int,
    emails: list[str],
    max_time: float,
) -> str:
    """Generate a .pbs script for Portable Batch System (PBS)."""
    lines = [
        _clusters(processors=processors),
        _name(fds_file=fds_file),
        _max_time(max_time=max_time),
        _shell(),
        _email(emails=emails),
        "#PBS -j oe",
        _module_load(version=version),
        _setup(),
        _commands(fds_file=fds_file),
    ]
    return "\n".join([line for line in lines if line.strip()])


def write_pbs(
    fds_file: Path,
    version: str,
    processors: int,
    emails: list[str],
    max_time: float,
) -> None:
    """Write a .pbs file."""
    text = generate_pbs(
        fds_file=fds_file,
        version=version,
        processors=processors,
        emails=emails,
        max_time=max_time,
    )
    fds_file.with_suffix(".pbs").write_text(text)
