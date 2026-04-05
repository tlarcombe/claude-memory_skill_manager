"""Entry point — launches TUI by default; subcommands available for scripting."""

from __future__ import annotations

import click

from claude_manager.agents.cli import agents
from claude_manager.mcp.cli import mcp
from claude_manager.memory.cli import memory
from claude_manager.skills.cli import skills


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def main(ctx: click.Context) -> None:
    """Claude Manager — manage Claude Code addons.

    Run without arguments to launch the interactive TUI.
    Use subcommands for scripting.
    """
    if ctx.invoked_subcommand is None:
        from claude_manager.tui import run
        run()


main.add_command(memory)
main.add_command(skills)
main.add_command(agents)
main.add_command(mcp)
