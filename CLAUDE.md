# Claude Manager — Claude Code Context

## Project Purpose

A CLI tool (Python) for managing Claude Code addons:
- **Memory** — read/write/delete `~/.claude/projects/*/memory/` entries
- **Skills** — browse/install/remove skills from `~/.claude/skills/`
- **Agents** — manage custom agents in `~/.claude/agents/`
- **MCP servers** — add/remove/configure entries in `~/.claude/settings.json`

## Project Layout

```
src/claude_manager/
├── cli.py          # Click group wiring all sub-commands
├── config.py       # Resolves ~/.claude paths
├── memory/         # models.py, store.py, cli.py
├── skills/         # models.py, store.py, cli.py
├── agents/         # models.py, store.py, cli.py
└── mcp/            # models.py, store.py, cli.py
tests/
```

Each domain follows the same three-file pattern: `models.py` (Pydantic), `store.py` (disk I/O), `cli.py` (Click commands).

## Key Conventions

- Python 3.11+, `pyproject.toml` / hatch build backend
- `click` for CLI, `rich` for output, `pydantic` v2 for models
- `ruff` for linting/formatting, `mypy --strict` for types
- `pytest` with `--cov-fail-under=80`
- No UI framework chosen yet — architecture is deferred

## Running

```bash
# Install in editable mode
uv pip install -e ".[dev]"

# Run CLI
claude-manager --help

# Tests
pytest
```
