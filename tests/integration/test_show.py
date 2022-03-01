"""Integration tests for the `xfds show` commands.

For xfds show versions, view appropriate test files in tests/services.
"""
from typer.testing import CliRunner

from xfds.cli import app

runner = CliRunner()


def test_show_nodes_command() -> None:
    """Test command displays list of Sabalcore nodes."""
    result = runner.invoke(app, ["show", "nodes"])
    assert result.exit_code == 0
    assert result.output.strip().startswith("node")
    assert len(result.output.splitlines()) == 8
