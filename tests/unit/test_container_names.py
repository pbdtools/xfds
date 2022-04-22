"""Tests for the container name.

There would be conflicts if two interactive containers for a specific FDS version
were running at the same time. This tests that the container name calls uuid.uuid4
to generate a unique name.
"""
from datetime import datetime
from pathlib import Path

from freezegun import freeze_time

from xfds import config
from xfds.core import container_name

DATE = "2021-12-31 3:14:15"
TIMESTAMP = datetime.strptime(DATE, "%Y-%m-%d %H:%M:%S").strftime(
    config.CONTAINER_TIMESTAMP_FORMAT
)


@freeze_time(DATE)
def test_interactive_name(latest: str, fds_file: Path) -> None:
    """Test interactive mode has unique name."""

    name = container_name(
        fds_file=fds_file,
        interactive=True,
        version=latest,
    )

    assert "fds" in name
    assert fds_file.stem not in name
    assert latest in name
    assert TIMESTAMP in name


@freeze_time(DATE)
def test_non_interactive_name(latest: str, fds_file: Path) -> None:
    """Test interactive mode has unique name."""

    name = container_name(
        fds_file=fds_file,
        interactive=False,
        version=latest,
    )

    assert "fds" not in name
    assert fds_file.stem in name
    assert latest in name
    assert TIMESTAMP in name
