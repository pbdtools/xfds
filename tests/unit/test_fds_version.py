"""Tests for determining the FDS version."""
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from xfds._run import fds_version, image_name


# - From Function Signature
def test_latest_by_default(latest: str, fds_file: Path) -> None:
    """Test default FDS version is latest."""
    version = fds_version(fds_file=fds_file)
    assert version == "latest"


def test_latest_if_specified(latest: str, fds_file: Path) -> None:
    """Test latest FDS version is specified."""
    version = fds_version(fds_file=fds_file, version=latest)
    assert version == latest


def test_older_if_specified(fds_file: Path) -> None:
    """Test older FDS version is specified."""
    requested = "6.2.0"
    version = fds_version(fds_file=fds_file, version=requested)
    assert version == requested


# - From metadata and file path
def test_extracts_fds_version_from_file_metadata(meta_dir: Path) -> None:
    """Test FDS version is extracted from metadata."""
    for fds_file in meta_dir.glob("*.fds"):
        version = fds_version(fds_file=fds_file)
        assert version == fds_file.stem


def test_cli_version_overrides_metadata_version(meta_dir: Path, latest: str) -> None:
    """Test CLI version overrides metadata version."""
    fds_file = meta_dir / "6.2.0.fds"
    version = fds_version(fds_file=fds_file, version=latest)
    assert version == latest


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
    version = fds_version(fds_file=fds_file)
    assert version == "1.2.3"


def test_metadata_overrides_file_path(meta_dir: Path) -> None:
    """Test that the version specified in metadata takes precidence."""
    fds_file = meta_dir / "6.7.5" / "test.fds"
    version = fds_version(fds_file=fds_file)
    assert version == "6.7.1"


# Image Name
def test_image_name_defaults_to_latest(latest: str) -> None:
    """Test defaults to latest FDS version."""
    image = image_name()
    assert latest not in image


def test_image_name_with_latest(latest: str) -> None:
    """Test latest FDS version is specified."""
    image = image_name(version=latest)
    assert latest in image


def test_image_name_with_older() -> None:
    """Test latest FDS version is specified."""
    requested = "6.2.0"
    image = image_name(version=requested)
    assert requested in image
