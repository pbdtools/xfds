"""Base API for DockerHub."""
from __future__ import annotations

from xfds.services.api import BaseAPI


class DockerHub(BaseAPI):
    def __init__(self, org: str, repo: str) -> None:
        self.org = org
        self.repo = repo
        self.base_url = f"https://hub.docker.com/v2/repositories/{org}/{repo}"

    def _data_from_page(self, data: dict) -> dict:
        """Extact data from page.

        Assumes that the whole response is a list of data.
        """
        return data["results"]

    def _tag_data(self, ascending: bool = False) -> list[dict]:
        """Get data Docker Hub's /tags endpoint."""
        endpoint = "/tags"
        params = dict(ordering={"-name" if ascending else "name"})
        data = self.get(endpoint, params)
        return data

    def tag_list(self, ascending: bool = False) -> list[str]:
        """Get list of tags from Docker Hub."""
        data = self._tag_data(ascending=ascending)
        return [
            tag["name"]
            for tag in data
            if "-" not in tag["name"] and tag["name"] != "latest"
        ]

    def latest_tag(self) -> str:
        """Get latest tag from Docker Hub."""
        data = self.tag_list()
        return data[0]
