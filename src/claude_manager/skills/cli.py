"""CLI commands for skill management."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claude_manager.skills.store import list_global_skills, list_project_skills

console = Console()


@click.group()
def skills() -> None:
    """Manage Claude Code skills."""


@skills.command("list")
@click.option("--project", "-p", type=click.Path(exists=True, file_okay=False, path_type=Path), default=None)
@click.option("--search", "-s", default=None, help="Filter by name or description.")
def list_cmd(project: Path | None, search: str | None) -> None:
    """List skills (global by default, or project-local with --project)."""
    items = list_project_skills(project) if project else list_global_skills()
    if search:
        term = search.lower()
        items = [s for s in items if term in s.name.lower() or term in s.description.lower()]
    if not items:
        console.print("[yellow]No skills found.[/yellow]")
        return
    scope = project.name if project else "global"
    table = Table(title=f"Skills ({scope})", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Description")
    table.add_column("Path", style="dim")
    for s in items:
        table.add_row(s.name, s.description, str(s.path))
    console.print(table)
