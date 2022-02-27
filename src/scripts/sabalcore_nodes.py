"""Get Node Information from Sabalcore."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import subprocess  # noqa: S404

from dotenv import load_dotenv
from slugify import slugify

from xfds.settings import SABALCORE_NODES_FILE

load_dotenv()
HOST = os.environ["SABALCORE_HOST"]
USER = os.environ["SABALCORE_USER"]
IGNORE_FIELDS = ["avail-cores"]
IGNORE_NODES = ["graphics"]


def get_output(command: str, host: str = HOST, user: str = USER) -> str:
    """Get output from ssh command."""
    proc = subprocess.Popen(
        f"ssh {user}@{host} {command}",
        shell=True,  # noqa: S602
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, _ = proc.communicate()
    return out.decode("utf-8")


def node_info_to_csv(node_info: str) -> str:
    """Format node info."""
    # Ignore available node summary and remove header separator
    node_info = node_info.replace("(0x(B", ",")
    node_info = node_info.replace("(0 (B", "")

    lines = node_info.split("\n")
    lines = lines[: lines.index("")]
    lines.pop(1)

    node_info = "\n".join(lines)
    return node_info


def normalize_value(field: str, value: str) -> str | int | float:
    """Normalize value.

    Convert to number if applicable. Removes units.
    """
    match = re.match(r"[\d\.]+", value)
    if match:
        num = match.group(0)
        try:
            return int(num)
        except ValueError:
            return float(num)
    return value


def csv_to_dict(csv_text: str) -> dict:
    """Convert CSV to JSON.

    After parsing data, this transposes the data so that the nodes are
    the keys and the fields are the values.
    """
    rows = []
    with io.StringIO(csv_text) as csv_data:
        reader = csv.DictReader(csv_data)
        for row in reader:
            if not row:
                break
            rows.append({k.strip(): v.strip() for k, v in row.items()})

    data: dict = {k: {} for k in rows[0].keys() if k}
    for row in rows:
        field = slugify(row[""])
        if field in IGNORE_FIELDS:
            continue
        for k, v in row.items():
            if k == "":
                continue
            data[k][field] = normalize_value(field, v)

    for node in IGNORE_NODES:
        if node in data:
            del data[node]

    return data


def get_node_info() -> dict:
    """Get node info."""
    node_info = get_output(command="upnodes")
    node_info = node_info_to_csv(node_info)
    return csv_to_dict(node_info)


def update_node_info() -> None:
    """Update node info."""
    SABALCORE_NODES_FILE.write_text(json.dumps(get_node_info(), indent=4))


if __name__ == "__main__":
    update_node_info()
