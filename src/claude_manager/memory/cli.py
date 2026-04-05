"""CLI commands for memory management."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claude_manager.memory.store import list_all_projects, list_entries

console = Console()


@click.group()
def memory() -> None:
    """Manage Claude Code memory files."""


@memory.command("list")
@click.option("--project", "-p", default=None, help="Project slug or path to filter by.")
def list_cmd(project: str | None) -> None:
    """List memory entries."""
    project_path = Path(project) if project else None
    entries = list_entries(project_path)
    if not entries:
        console.print("[yellow]No memory entries found.[/yellow]")
        return
    table = Table(title="Memory Entries", show_lines=True)
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Project", style="dim")
    for e in entries:
        table.add_row(e.type.value, e.name, e.description, e.project or "")
    console.print(table)


@memory.command("projects")
def projects_cmd() -> None:
    """List all projects that have memory entries."""
    projects = list_all_projects()
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    for p in projects:
        console.print(f"  [cyan]{p}[/cyan]")
