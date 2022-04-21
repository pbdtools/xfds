"""Functions for formatting messages.

This module allows for messages to be consistently formatted by
message type. Some message types are always printed, while others
are only printed if verbose mode is enabled.

By default, error, warning, and success messages are always printed
while info and debug messages are not. To modify the behavior for
a specific message in a different module, set `always` to True
or False as needed.
"""
import typer

from . import config


def _echo(icon: str, msg: str, fg: str, always: bool) -> None:
    """Print message."""
    if config.MESSAGE_ICONS:
        msg = f"{icon}  {msg}"
    if always or config.VERBOSE:
        typer.echo(typer.style(msg, fg=fg))


def error(msg: str, always: bool = True, icon: str = "❌") -> None:
    """Print error message."""
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.RED)


def warning(msg: str, always: bool = True, icon: str = "⚠️ ") -> None:
    """Print warning message."""
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.YELLOW)


def info(msg: str, always: bool = False, icon: str = "") -> None:
    """Print info message."""
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.BLUE)


def debug(msg: str, always: bool = False, icon: str = "🐞") -> None:
    """Print debug message."""
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.MAGENTA)


def success(msg: str, always: bool = True, icon: str = "✔️ ") -> None:
    """Print success message."""
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.GREEN)


def section(msg: str, always: bool = False, icon: str = "📑") -> None:
    """Print section header message."""
    msg = f"===== {msg} ====="
    _echo(icon=icon, msg=msg, always=always, fg=typer.colors.BRIGHT_CYAN)
