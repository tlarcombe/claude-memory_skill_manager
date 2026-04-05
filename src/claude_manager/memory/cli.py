"""CLI commands for memory management."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claude_manager.config import all_memory_project_slugs
from claude_manager.memory.store import list_entries

console = Console()


@click.group()
def memory() -> None:
    """Manage Claude Code memory files."""


@memory.command("list")
@click.argument("project", type=click.Path(exists=True, file_okay=False, path_type=Path))
def list_cmd(project: Path) -> None:
    """List memory entries for PROJECT path."""
    entries = list_entries(project)
    if not entries:
        console.print("[yellow]No memory entries found.[/yellow]")
        return
    table = Table(title=f"Memory: {project.name}", show_lines=True)
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold")
    table.add_column("Description")
    for e in entries:
        table.add_row(e.type.value, e.name, e.description)
    console.print(table)


@memory.command("projects")
def projects_cmd() -> None:
    """List all projects that have memory entries."""
    slugs = all_memory_project_slugs()
    if not slugs:
        console.print("[yellow]No projects found.[/yellow]")
        return
    for s in slugs:
        console.print(f"  [cyan]{s}[/cyan]")
