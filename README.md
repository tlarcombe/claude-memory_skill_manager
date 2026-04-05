# claude-manager

A manager for Claude Code addons: **memory**, **skills**, **agents**, and **MCP servers**.

Browse, inspect, add, and remove the files and configuration that power your Claude Code setup — from a single CLI.

---

## Status

Early development. The current version provides read-only listing for all four domains. Write operations (add, remove, edit) are next.

## Installation

Requires Python 3.11+.

```bash
# With uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

## Usage

```bash
# List all memory entries for a project
claude-manager memory list --project /path/to/project

# List all projects with memory
claude-manager memory projects

# List installed skills
claude-manager skills list
claude-manager skills list --search "debugging"

# List custom agents
claude-manager agents list

# List configured MCP servers
claude-manager mcp list
```

## Development

```bash
# Run tests
pytest

# Lint + format
ruff check src tests
ruff format src tests

# Type check
mypy src
```

## Project structure

```
src/claude_manager/
├── cli.py          # Top-level CLI entry point
├── config.py       # Path resolution for ~/.claude directories
├── memory/         # Memory file management
├── skills/         # Skill file management
├── agents/         # Agent file management
└── mcp/            # MCP server configuration management
```

## License

MIT
