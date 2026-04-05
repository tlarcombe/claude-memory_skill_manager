"""CLI commands for skill management."""

import click
from rich.console import Console
from rich.table import Table

from claude_manager.skills.store import list_skills

console = Console()


@click.group()
def skills() -> None:
    """Manage Claude Code skills."""


@skills.command("list")
@click.option("--search", "-s", default=None, help="Filter by name or description.")
def list_cmd(search: str | None) -> None:
    """List installed skills."""
    all_skills = list_skills()
    if search:
        term = search.lower()
        all_skills = [
            s for s in all_skills if term in s.name.lower() or term in s.description.lower()
        ]
    if not all_skills:
        console.print("[yellow]No skills found.[/yellow]")
        return
    table = Table(title="Installed Skills", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Description")
    table.add_column("Path", style="dim")
    for s in all_skills:
        table.add_row(s.name, s.description, str(s.path))
    console.print(table)
