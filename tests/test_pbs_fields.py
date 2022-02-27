"""Test ability to select correct file or folder."""
from pathlib import Path
from textwrap import dedent

import pytest

from xfds import pbs

CLUSTERS = {
    "cfast": {
        "cores-node": 2,
        "total-cores": 4,
    },
    "fds": {
        "cores-node": 8,
        "total-cores": 64,
    },
    "pbd": {
        "cores-node": 16,
        "total-cores": 128,
    },
    "tools": {
        "cores-node": 42,
        "total-cores": 126,
    },
}


def test_clusters() -> None:
    text = pbs._clusters(cores=42, node_list=CLUSTERS)
    expected = dedent(
        """
        #PBS -l nodes=5:fds:ppn=8:1:fds:ppn=2
        #PBS -l nodes+=2:pbd:ppn=16:1:pbd:ppn=10
        #PBS -l nodes++=1:tools:ppn=42
        """
    )
    assert text.strip() == expected.strip()


def test_name_is_from_input_file(fds_file: Path) -> None:
    """Test that name is from input file."""
    text = pbs._name(fds_file=fds_file)
    assert fds_file.stem in text


def test_name_raies_error_when_passed_directory(empty_dir: Path) -> None:
    """Test that name raises error when passed directory."""
    with pytest.raises(TypeError):
        pbs._name(fds_file=empty_dir)


def test_email_is_blank_when_not_specified() -> None:
    """Test that email is blank when not specified."""
    email = pbs._email()
    assert email == ""


def test_email_format_with_single_email_address() -> None:
    """Test that email is formatted correctly."""
    emails = ["fds@pbd.tools"]
    text = pbs._email(emails=emails)
    assert "#PBS -m abe" in text
    for email in emails:
        assert email in text


def test_email_format_with_multiple_email_addresses() -> None:
    """Test that email is formatted correctly."""
    emails = ["fds@pbd.tools", "pbd@pbd.tools"]
    text = pbs._email(emails=emails)
    assert "#PBS -m abe" in text
    for email in emails:
        assert email in text


def test_shell_is_bash_when_not_specified() -> None:
    """Test that shell is bash when not specified."""
    text = pbs._shell()
    assert text == "#PBS -S /bin/bash"


def test_shell_is_bash_when_none_is_specified() -> None:
    """Test that shell is bash when not specified."""
    text = pbs._shell(shell=None)
    assert text == "#PBS -S /bin/bash"


def test_shell_when_specified() -> None:
    """Test that shell is bash when not specified."""
    shell = "/bin/zsh"
    text = pbs._shell(shell=shell)  # noqa: S604
    assert text == f"#PBS -S {shell}"


def test_max_time_is_empty_when_max_time_is_zero() -> None:
    """Test that max_time is empty when max_time is zero."""
    text = pbs._max_time(max_time=0)
    assert text == ""


def test_max_time_is_empty_when_max_time_is_negative() -> None:
    """Test that max_time is empty when max_time is negative."""
    text = pbs._max_time(max_time=-1)
    assert text == ""


@pytest.mark.parametrize(
    "hours, hhmmss",
    [
        (0.25, "0:15:00"),
        (1.00, "1:00:00"),
        (1.50, "1:30:00"),
        (10.75, "10:45:00"),
    ],
)
def test_max_time_when_max_time_is_specified(hours: float, hhmmss: str) -> None:
    """Test that max_time is formatted correctly."""
    text = pbs._max_time(max_time=hours)
    assert text == f"#PBS -l walltime={hhmmss}"


@pytest.mark.parametrize(
    "version, module",
    [
        ("", "fds"),
        ("latest", "fds"),
        ("6.7.7", "fds/6.7.7"),
        ("6.7.5", "fds/6.7.5"),
    ],
)
def test_load_module_specified_correctly(version: str, module: str) -> None:
    """Test that fds_module is formatted correctly."""
    text = pbs._module_load(version=version)
    assert module == text.strip().split()[-1]
