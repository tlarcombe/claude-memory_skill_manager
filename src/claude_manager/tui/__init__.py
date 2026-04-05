"""TUI entry point — hierarchical fzf navigator for Claude Code addons."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from claude_manager.tui.fzf import set_title
from claude_manager.tui.screens import run_main, run_scope, run_tools


def _view_file(path_str: str) -> None:
    """Open a file in $EDITOR or fall back to less."""
    editor = os.environ.get("EDITOR", "")
    if editor:
        subprocess.run([editor, path_str])
    else:
        subprocess.run(["less", path_str])


def _confirm_delete(name: str) -> bool:
    print(f"\n  Delete: {name}")
    answer = input("  Confirm? [y/N] ").strip().lower()
    print()
    return answer in ("y", "yes")


def _delete_tool(scope: str, tool_type: str, key: str) -> None:
    """Delete a tool entry (file or settings key)."""
    from claude_manager.config import global_settings_path, project_settings_path
    import json

    name = Path(key).name if "/" in key else key

    if tool_type == "mcp":
        # Remove from settings.json
        is_global = scope == "GLOBAL"
        settings = global_settings_path() if is_global else project_settings_path(Path(scope))
        if not settings.exists():
            return
        try:
            data = json.loads(settings.read_text())
        except (json.JSONDecodeError, OSError):
            return
        servers = data.get("mcpServers", {})
        if key not in servers:
            print(f"  Not found: {key}")
            return
        if _confirm_delete(key):
            del servers[key]
            data["mcpServers"] = servers
            settings.write_text(json.dumps(data, indent=2))
            print(f"  Removed MCP server: {key}")
    else:
        # File-based tool (skill, agent, memory entry)
        target = Path(key)
        if not target.exists():
            print(f"  File not found: {key}")
            return
        if _confirm_delete(name):
            target.unlink()
            print(f"  Deleted: {key}")

    input("  Press Enter to continue...")


def run() -> None:
    """Main TUI application loop."""
    if not _fzf_available():
        print("Error: fzf not found. Install with: sudo pacman -S fzf", file=sys.stderr)
        sys.exit(1)

    set_title("claude-manager")

    while True:
        os.system("clear")
        result = run_main()
        if result is None:
            break  # Esc / quit

        scope, pressed = result

        # Ctrl-I on main screen → install flow (future)
        if pressed == "ctrl-i":
            print(f"\n  Install from registry: coming soon.\n")
            input("  Press Enter to continue...")
            continue

        # Drill into scope
        while True:
            os.system("clear")
            scope_result = run_scope(scope)
            if scope_result is None:
                break  # back to main

            sc, tool_type, sc_pressed = scope_result

            # Drill into tool list
            while True:
                os.system("clear")
                tools_result = run_tools(sc, tool_type)
                if tools_result is None:
                    break  # back to scope

                _scope, _type, key, t_pressed = tools_result

                if t_pressed == "ctrl-d":
                    os.system("clear")
                    _delete_tool(_scope, _type, key)
                elif _type != "mcp":
                    _view_file(key)
                else:
                    print(f"\n  MCP server: {key}\n  (edit ~/.claude/settings.json to modify)\n")
                    input("  Press Enter to continue...")

    set_title("terminal")


def _fzf_available() -> bool:
    import shutil
    return shutil.which("fzf") is not None
