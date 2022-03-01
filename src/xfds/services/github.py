"""Base API for Github."""
from __future__ import annotations

from xfds.services.api import BaseAPI


class Github(BaseAPI):
    def __init__(self, org: str, repo: str) -> None:
        self.org = org
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{org}/{repo}"

    def _release_data(self) -> list[dict]:
        """Get data Github's /releases endpoint."""
        endpoint = "/releases"
        data = self.get(endpoint)
        return data

    def tag_list(self) -> list[str]:
        """Get list of tags from releases."""
        data = self._release_data()
        return [release["tag_name"] for release in data if "FDS" in release["tag_name"]]

    def latest_tag(self) -> str:
        """Get latest tag from Github."""
        data = self.tag_list()
        return data[0]
