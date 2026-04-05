"""CLI commands for agent management."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claude_manager.agents.store import list_global_agents, list_project_agents

console = Console()


@click.group()
def agents() -> None:
    """Manage Claude Code agents."""


@agents.command("list")
@click.option("--project", "-p", type=click.Path(exists=True, file_okay=False, path_type=Path), default=None)
def list_cmd(project: Path | None) -> None:
    """List agents (global by default, or project-local with --project)."""
    items = list_project_agents(project) if project else list_global_agents()
    if not items:
        console.print("[yellow]No agents found.[/yellow]")
        return
    scope = project.name if project else "global"
    table = Table(title=f"Agents ({scope})", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Description")
    table.add_column("Model", style="dim")
    for a in items:
        table.add_row(a.name, a.description, a.model or "")
    console.print(table)
