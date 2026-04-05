"""Top-level CLI entry point."""

import click

from claude_manager.agents.cli import agents
from claude_manager.mcp.cli import mcp
from claude_manager.memory.cli import memory
from claude_manager.skills.cli import skills


@click.group()
@click.version_option()
def main() -> None:
    """Claude Manager — manage Claude Code addons."""


main.add_command(memory)
main.add_command(skills)
main.add_command(agents)
main.add_command(mcp)
