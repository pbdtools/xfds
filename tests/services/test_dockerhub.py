"""Test calls to Docker Hub."""
from __future__ import annotations

import json

import requests
from _pytest.monkeypatch import MonkeyPatch

from xfds.docker_hub import tags

from . import DATADIR


class MockTags:
    """Mock the requests.get function."""

    def __init__(self, url: str) -> None:
        pass

    def json(self) -> list[str]:
        """Return pre-fetched api response."""
        json_file = DATADIR / "dockerhub" / "tags.json"
        return json.loads(json_file.read_text())


def test_filters_os_specific_tags(monkeypatch: MonkeyPatch) -> None:
    """Test only version tags are returned."""
    monkeypatch.setattr(requests, "get", MockTags)

    assert tags() == ["latest", "6.7.7", "6.7.6"]
