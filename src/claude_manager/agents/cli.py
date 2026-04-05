"""CLI commands for agent management."""

import click
from rich.console import Console
from rich.table import Table

from claude_manager.agents.store import list_agents

console = Console()


@click.group()
def agents() -> None:
    """Manage Claude Code agents."""


@agents.command("list")
def list_cmd() -> None:
    """List installed agents."""
    all_agents = list_agents()
    if not all_agents:
        console.print("[yellow]No agents found.[/yellow]")
        return
    table = Table(title="Installed Agents", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Description")
    table.add_column("Model", style="dim")
    table.add_column("Tools", style="dim")
    for a in all_agents:
        table.add_row(
            a.name,
            a.description,
            a.model or "",
            ", ".join(a.tools) if a.tools else "",
        )
    console.print(table)
