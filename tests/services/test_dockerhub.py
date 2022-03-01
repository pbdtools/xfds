"""Test calls to Docker Hub."""
from __future__ import annotations

import json

from _pytest.monkeypatch import MonkeyPatch

from xfds.services.dockerhub import DockerHub

from . import DATADIR


def mock_get_page(*args, **kwargs) -> list[str]:
    """Return pre-fetched api response."""
    json_file = DATADIR / "dh_openbcl_fds_tags.json"
    return json.loads(json_file.read_text())


def test_filters_os_specific_tags(monkeypatch: MonkeyPatch) -> None:
    """Test only version tags are returned."""
    monkeypatch.setattr(DockerHub, "get_page", mock_get_page)
    dh_openbcl_fds = DockerHub("openbcl", "fds")

    assert dh_openbcl_fds.tag_list() == ["6.7.7", "6.7.6"]
