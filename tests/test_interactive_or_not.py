"""Tests for determining if the container should be run in interactive mode."""
from pathlib import Path

from xfds.core import build_arguments


# Interactive
def test_interactive_if_interactive_true_with_fds_file(fds_file: Path) -> None:
    """Test container is interactive when interactive and fds file are specified."""
    cmd = build_arguments(interactive=True, fds_file=fds_file)
    assert "-it" in cmd


def test_interactive_if_interactive_true_with_fds_dir(fds_dir: Path) -> None:
    """Test container is interactive when interactive and fds dir are specified."""
    cmd = build_arguments(interactive=True, fds_file=fds_dir)
    assert "-it" in cmd


def test_interactive_if_interactive_true_with_empty_dir(empty_dir: Path) -> None:
    """Test container is interactive when interactive and empty dir are specified."""
    cmd = build_arguments(interactive=True, fds_file=empty_dir)
    assert "-it" in cmd


def test_interactive_if_interactive_false_with_empty_dir(empty_dir: Path) -> None:
    """Test container is not interactive when empty dir is specified and interactive is false."""
    cmd = build_arguments(interactive=False, fds_file=empty_dir)
    assert "-it" in cmd


# Non-interactive
def test_not_interactive_if_interactive_false_with_fds_file(fds_file: Path) -> None:
    """Test container is not interactive when fds file is specified and interactive is false."""
    cmd = build_arguments(interactive=False, fds_file=fds_file)
    assert "-it" not in cmd


def test_not_interactive_if_interactive_false_with_fds_dir(fds_dir: Path) -> None:
    """Test container is not interactive when fds dir is specified and interactive is false."""
    cmd = build_arguments(interactive=False, fds_file=fds_dir)
    assert "-it" not in cmd
