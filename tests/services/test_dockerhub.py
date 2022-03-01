"""Test calls to Docker Hub."""
from __future__ import annotations

import json

from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner

from xfds.cli import app
from xfds.services.dockerhub import DockerHub

from . import DATADIR

runner = CliRunner()


def mock_get_page(*args, **kwargs) -> list[str]:
    """Return pre-fetched api response."""
    json_file = DATADIR / "dh_openbcl_fds_tags.json"
    return json.loads(json_file.read_text())


def test_filters_os_specific_tags(monkeypatch: MonkeyPatch) -> None:
    """Test only version tags are returned."""
    monkeypatch.setattr(DockerHub, "get_page", mock_get_page)
    dh_openbcl_fds = DockerHub("openbcl", "fds")

    assert dh_openbcl_fds.tag_list() == ["6.7.7", "6.7.6"]


def test_cli_show_versions_images(monkeypatch: MonkeyPatch) -> None:
    """Test CLI show versions fds command."""
    monkeypatch.setattr(DockerHub, "get_page", mock_get_page)
    result = runner.invoke(app, ["show", "versions", "images"])
    assert result.exit_code == 0
    assert "latest" not in result.output
    assert len(result.output.split(",")) == 2


def test_cli_show_versions_latest_image(monkeypatch: MonkeyPatch) -> None:
    """Test CLI show versions fds command."""
    monkeypatch.setattr(DockerHub, "get_page", mock_get_page)
    result = runner.invoke(app, ["show", "versions", "--latest", "images"])
    assert result.exit_code == 0
    assert "latest" not in result.output
    assert result.output.strip() == "6.7.7"
