"""Tests for determining the FDS version."""
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from xfds.core import build_arguments


def format_image_name(fds_version: str) -> str:
    """Return the image name for the specified FDS version."""
    return f"openbcl/fds:{fds_version}"


def extract_container_name(cmd: list) -> str:
    """Extract the container name from the command line."""
    return [arg for arg in cmd if "openbcl/fds" in arg][0]


def test_latest_by_default(latest: str, fds_file: Path) -> None:
    """Test default FDS version is latest."""
    cmd = build_arguments(fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)


def test_latest_if_specified(latest: str, fds_file: Path) -> None:
    """Test latest FDS version is specified."""
    cmd = build_arguments(version=latest, fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)


def test_older_if_specified(fds_file: Path) -> None:
    """Test older FDS version is specified."""
    cmd = build_arguments(version="6.2.0", fds_file=fds_file)
    assert format_image_name("6.2.0") == extract_container_name(cmd)


def test_extracts_fds_version_from_file_metadata(meta_dir: Path) -> None:
    """Test FDS version is extracted from metadata."""
    for fds_file in meta_dir.glob("*.fds"):
        cmd = build_arguments(fds_file=fds_file)
        assert format_image_name(fds_file.stem) == extract_container_name(cmd)


def test_cli_version_overrides_metadata_version(meta_dir: Path, latest: str) -> None:
    """Test CLI version overrides metadata version."""
    fds_file = meta_dir / "6.2.0.fds"
    cmd = build_arguments(version=latest, fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)


paths = [
    Path("path/to/1_2_3/case/"),
    Path("path/to/1.2.3/case/"),
    Path("path/to/v1_2_3/case/"),
    Path("path/to/v1.2.3/case/"),
    Path("path/to/fds_1_2_3/case/"),
    Path("path/to/fds.1.2.3/case/"),
    Path("path/to/fds_1.2.3/case/"),
]


@pytest.mark.parametrize(
    "fds_file",
    paths,
    ids=[path.parts[-2] for path in paths],
)
def test_pulls_version_from_file_path(monkeypatch: MonkeyPatch, fds_file: Path) -> None:
    """Test FDS version is extracted from file path."""

    def image_name_from_command(command: list) -> str:
        name = [item for item in command if "openbcl/fds" in item][0]
        return name.replace("-", ".").replace("_", ".")

    cmd = build_arguments(fds_file=fds_file)
    assert format_image_name("1.2.3") == image_name_from_command(cmd)


def test_metadata_overrides_file_path(meta_dir: Path) -> None:
    """Test that the version specified in metadata takes precidence."""
    fds_file = meta_dir / "6.7.5" / "test.fds"
    cmd = build_arguments(fds_file=fds_file)
    assert format_image_name("6.7.1") == extract_container_name(cmd)
