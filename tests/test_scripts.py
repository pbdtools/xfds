"""Ensure maintenance scripts have ran."""
from scripts import usage


def test_usage_file_is_current() -> None:
    """Ensure USAGE.md is up to date."""
    assert usage.compile_text() == usage.USAGE_FILE.read_text()
