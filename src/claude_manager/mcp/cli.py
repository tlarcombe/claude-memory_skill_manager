"""CLI commands for MCP server management."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from claude_manager.mcp.store import list_global_servers, list_project_servers

console = Console()


@click.group()
def mcp() -> None:
    """Manage Claude Code MCP servers."""


@mcp.command("list")
@click.option("--project", "-p", type=click.Path(exists=True, file_okay=False, path_type=Path), default=None)
def list_cmd(project: Path | None) -> None:
    """List MCP servers (global by default, or project-local with --project)."""
    servers = list_project_servers(project) if project else list_global_servers()
    if not servers:
        console.print("[yellow]No MCP servers configured.[/yellow]")
        return
    scope = project.name if project else "global"
    table = Table(title=f"MCP Servers ({scope})", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Command")
    table.add_column("Args", style="dim")
    table.add_column("Env vars", style="dim")
    for s in servers:
        table.add_row(s.name, s.command, " ".join(s.args), ", ".join(s.env.keys()) if s.env else "")
    console.print(table)
