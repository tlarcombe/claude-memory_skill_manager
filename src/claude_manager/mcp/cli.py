"""CLI commands for MCP server management."""

import click
from rich.console import Console
from rich.table import Table

from claude_manager.mcp.store import list_servers

console = Console()


@click.group()
def mcp() -> None:
    """Manage Claude Code MCP servers."""


@mcp.command("list")
def list_cmd() -> None:
    """List configured MCP servers."""
    servers = list_servers()
    if not servers:
        console.print("[yellow]No MCP servers configured.[/yellow]")
        return
    table = Table(title="MCP Servers", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Command")
    table.add_column("Args", style="dim")
    table.add_column("Env vars", style="dim")
    for s in servers:
        table.add_row(
            s.name,
            s.command,
            " ".join(s.args),
            ", ".join(s.env.keys()) if s.env else "",
        )
    console.print(table)
