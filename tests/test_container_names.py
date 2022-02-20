"""Tests for the container name.

There would be conflicts if two interactive containers for a specific FDS version
were running at the same time. This tests that the container name calls uuid.uuid4
to generate a unique name.
"""
import uuid
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

from xfds.core import container_name


def patch_uuid() -> str:
    """Patch uuid.uuid4 to return a fixed value."""
    return "p4x-639"


def test_interactive_name(
    monkeypatch: MonkeyPatch, latest: str, fds_file: Path
) -> None:
    """Test interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)

    name = container_name(
        fds_file=fds_file,
        interactive=True,
        version=latest,
    )

    assert "fds" in name
    assert fds_file.stem not in name
    assert latest in name
    assert patch_uuid() in name


def test_non_interactive_name(
    monkeypatch: MonkeyPatch, latest: str, fds_file: Path
) -> None:
    """Test interactive mode has unique name."""
    monkeypatch.setattr(uuid, "uuid4", patch_uuid)

    name = container_name(
        fds_file=fds_file,
        interactive=False,
        version=latest,
    )

    assert "fds" not in name
    assert fds_file.stem in name
    assert latest in name
    assert patch_uuid() in name
