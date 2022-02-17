"""Tests for determining if the container should be run in interactive mode."""
from pathlib import Path

from xfds.core import interactive_mode


def test_interactive_if_interactive_true_with_fds_file(fds_file: Path) -> None:
    """Test container is interactive when interactive and fds file are specified."""
    assert interactive_mode(fds_file=fds_file, interactive=True)


def test_interactive_if_interactive_true_with_fds_dir(fds_dir: Path) -> None:
    """Test container is interactive when interactive and fds dir are specified."""
    assert interactive_mode(fds_file=fds_dir, interactive=True)


def test_interactive_if_interactive_true_with_empty_dir(empty_dir: Path) -> None:
    """Test container is interactive when interactive and empty dir are specified."""
    assert interactive_mode(fds_file=empty_dir, interactive=True)


def test_not_interactive_if_interactive_false_with_fds_file(fds_file: Path) -> None:
    """Test container is not interactive when fds file is specified and interactive is false."""
    assert not interactive_mode(fds_file=fds_file, interactive=False)


def test_not_interactive_if_interactive_false_with_fds_dir(fds_dir: Path) -> None:
    """Test container is not interactive when fds dir is specified and interactive is false."""
    assert interactive_mode(fds_file=fds_dir, interactive=False)


def test_interactive_if_interactive_false_with_empty_dir(empty_dir: Path) -> None:
    """Test container is not interactive when empty dir is specified and interactive is false."""
    assert interactive_mode(fds_file=empty_dir, interactive=False)
