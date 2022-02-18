"""Functions for getting data from Docker Hub."""
from __future__ import annotations

import requests

ORG = "openbcl"
REPO = "fds"
BASE_URL = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}"


def tags(ascending: bool = False) -> list[str]:
    """Get tags from Docker Hub.

    Filters out tags that are OS specific.
    """
    url = f"{BASE_URL}/tags?ordering={'-name' if ascending else 'name'}"

    tags = []
    while url:
        r = requests.get(url)
        tags.extend(r.json()["results"])
        url = r.json()["next"]

    return [tag["name"] for tag in tags if "-" not in tag["name"]]
