"""Tests for the container name.

There would be conflicts if two interactive containers for a specific FDS version
were running at the same time. This tests that the container name calls uuid.uuid4
to generate a unique name.
"""
import uuid
from pathlib import Path

from pytest.monkeypatch import MonkeyPatch

from xfds.core import build_arguments


def patch_uuid() -> str:
    """Patch uuid.uuid4 to return a fixed value."""
    return "p4x-639"


def test_interactive_name(monkeypatch: MonkeyPatch, latest: str) -> None:
    """Test interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)
    command = build_arguments(interactive=True)

    given = command[command.index("--name") + 1]
    expected = f"fds-{latest}-{patch_uuid()}"

    assert given == expected


def test_interactive_with_empty_dir(
    monkeypatch: MonkeyPatch, empty_dir: Path, latest: str
) -> None:
    """Test interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)
    command = build_arguments(fds_file=empty_dir)

    given = command[command.index("--name") + 1]
    expected = f"fds-{latest}-{patch_uuid()}"

    assert given == expected


def test_noninteractive_name_with_fds_file(
    monkeypatch: MonkeyPatch, fds_file: Path
) -> None:
    """Test non-interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)
    command = build_arguments(fds_file=fds_file)

    given = command[command.index("--name") + 1]
    expected = f"{fds_file.stem}-{patch_uuid()}"

    assert given == expected


def test_noninteractive_name_with_fds_dir(
    monkeypatch: MonkeyPatch, fds_dir: Path
) -> None:
    """Test non-interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)
    command = build_arguments(fds_file=fds_dir)

    given = command[command.index("--name") + 1]
    fds_file = next(fds_dir.glob("*.fds"))
    expected = f"{fds_file.stem}-{patch_uuid()}"

    assert given == expected
