"""Test calls to Docker Hub."""
from __future__ import annotations

import json

from _pytest.monkeypatch import MonkeyPatch

from xfds.services.github import Github

from . import DATADIR


def mock_get_page(*args, **kwargs) -> list[str]:
    """Return pre-fetched api response."""
    json_file = DATADIR / "gh_firemodels_fds_releases.json"
    return json.loads(json_file.read_text())


def test_named_releases(monkeypatch: MonkeyPatch) -> None:
    """Test only version tags are returned."""
    monkeypatch.setattr(Github, "get_page", mock_get_page)
    gh_firemodels_fds = Github("firemodels", "fds")
    expected = [
        "FDS6.7.7",
        "FDS6.7.6",
        "FDS6.7.5",
        "FDS6.7.4",
        "FDS6.7.3",
        "FDS6.7.1",
        "FDS6.7.0",
        "FDS6.6.0",
        "FDS6.5.3",
    ]
    assert gh_firemodels_fds.tag_list() == expected
