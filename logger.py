"""
Centralized logging with colored output.
"""
from rich.console import Console
from rich.logging import RichHandler
import logging
import sys

console = Console()


def get_logger(name: str = "mediroza") -> logging.Logger:
    """Return a configured logger with rich formatting."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    return logger


def banner(text: str) -> None:
    """Print a styled banner."""
    console.rule(f"[bold cyan]{text}[/bold cyan]")


def success(msg: str) -> None:
    console.print(f"[bold green][✓][/bold green] {msg}")


def warning(msg: str) -> None:
    console.print(f"[bold yellow][!][/bold yellow] {msg}")


def error(msg: str) -> None:
    console.print(f"[bold red][✗][/bold red] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    console.print(f"[bold blue][*][/bold blue] {msg}")