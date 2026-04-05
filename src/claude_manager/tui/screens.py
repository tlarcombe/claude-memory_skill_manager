"""TUI screen definitions — each function builds an fzf item list and handles the result."""

from __future__ import annotations

from pathlib import Path

from claude_manager.agents.store import list_global_agents, list_project_agents
from claude_manager.config import list_known_projects, memory_store_dir
from claude_manager.mcp.store import list_global_servers, list_project_servers
from claude_manager.memory.store import list_entries
from claude_manager.skills.store import list_global_skills, list_project_skills
from claude_manager.tui.fzf import (
    BOLD,
    BOLD_CYAN,
    BOLD_GREEN,
    DIM,
    GREEN,
    MAGENTA,
    RESET,
    YELLOW,
    FzfResult,
    fzf,
)

# ── Scope summary helpers ─────────────────────────────────────────────────────

def _count_str(n: int, label: str) -> str:
    return f"{YELLOW}{n}{RESET} {DIM}{label}{RESET}"


def _global_summary() -> str:
    sk = len(list_global_skills())
    ag = len(list_global_agents())
    mc = len(list_global_servers())
    parts = [
        _count_str(sk, "skills"),
        _count_str(ag, "agents"),
        _count_str(mc, "mcp"),
    ]
    return "  " + "  ".join(parts)


def _project_summary(project: Path) -> str:
    sk = len(list_project_skills(project))
    ag = len(list_project_agents(project))
    mc = len(list_project_servers(project))
    mem = len(list_entries(project))
    parts = []
    if sk:  parts.append(f"{DIM}sk:{RESET}{YELLOW}{sk}{RESET}")
    if ag:  parts.append(f"{DIM}ag:{RESET}{YELLOW}{ag}{RESET}")
    if mc:  parts.append(f"{DIM}mcp:{RESET}{YELLOW}{mc}{RESET}")
    if mem: parts.append(f"{DIM}mem:{RESET}{YELLOW}{mem}{RESET}")
    if not parts:
        return f"  {DIM}no local tools{RESET}"
    return "  " + "  ".join(parts)


# ── Screen 1: Main — scope selection ─────────────────────────────────────────

MAIN_HEADER = (
    f"  {BOLD_CYAN}claude-manager{RESET}  ·  manage Claude Code addons\n"
    f"  Enter: explore  Ctrl-I: install  Esc: quit"
)


def main_items() -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []

    # Global scope row
    summary = _global_summary()
    items.append((
        "GLOBAL",
        f"{BOLD_GREEN}[*]{RESET} {BOLD}GLOBAL{RESET}{summary}",
    ))

    # Separator
    items.append(("---", f"{DIM}────────────────────────────────────────{RESET}"))

    # Projects
    for project in list_known_projects():
        name = project.name
        summary = _project_summary(project)
        items.append((
            str(project),
            f"{GREEN}[-]{RESET} {BOLD_CYAN}{name}{RESET}{summary}",
        ))

    return items


def run_main() -> tuple[str, str] | None:
    """Returns (scope_key, pressed_key) or None to quit."""
    result = fzf(
        main_items(),
        header=MAIN_HEADER,
        prompt="  manager> ",
        expect=["ctrl-i"],
    )
    if not result.key or result.key == "---":
        return None
    return result.key, result.pressed


# ── Screen 2: Scope — tool type selection ────────────────────────────────────

_TOOL_TYPES = [
    ("skills",  "Skills",      MAGENTA),
    ("agents",  "Agents",      MAGENTA),
    ("mcp",     "MCP Servers", MAGENTA),
    ("memory",  "Memory",      MAGENTA),
]


def scope_items(scope: str) -> list[tuple[str, str]]:
    is_global = scope == "GLOBAL"
    project = Path(scope) if not is_global else None

    def count(kind: str) -> int:
        if kind == "skills":
            return len(list_global_skills() if is_global else list_project_skills(project))  # type: ignore[arg-type]
        if kind == "agents":
            return len(list_global_agents() if is_global else list_project_agents(project))  # type: ignore[arg-type]
        if kind == "mcp":
            return len(list_global_servers() if is_global else list_project_servers(project))  # type: ignore[arg-type]
        if kind == "memory":
            return 0 if is_global else len(list_entries(project))  # type: ignore[arg-type]
        return 0

    items: list[tuple[str, str]] = []
    for key, label, colour in _TOOL_TYPES:
        if is_global and key == "memory":
            # Memory is always project-scoped — show info row instead
            items.append((
                f"{scope}:memory",
                f"  {DIM}{label:<14}see per-project{RESET}",
            ))
            continue
        n = count(key)
        count_col = YELLOW if n > 0 else DIM
        items.append((
            f"{scope}:{key}",
            f"  {colour}{label:<14}{RESET}{count_col}{n:>3} {'installed' if not is_global else ''}{RESET}",
        ))

    return items


def scope_header(scope: str) -> str:
    label = "GLOBAL" if scope == "GLOBAL" else f"project: {Path(scope).name}"
    return (
        f"  {BOLD_CYAN}{label}{RESET}\n"
        f"  Enter: list  Esc: back"
    )


def run_scope(scope: str) -> tuple[str, str, str] | None:
    """Returns (scope, tool_type, pressed_key) or None to go back."""
    result = fzf(
        scope_items(scope),
        header=scope_header(scope),
        prompt="  type> ",
    )
    if not result.key:
        return None
    # key is "SCOPE:type"
    parts = result.key.split(":", 1)
    if len(parts) != 2:
        return None
    sc, tool_type = parts
    return sc, tool_type, result.pressed


# ── Screen 3: Tool list ───────────────────────────────────────────────────────

def tool_items(scope: str, tool_type: str) -> list[tuple[str, str]]:
    is_global = scope == "GLOBAL"
    project = Path(scope) if not is_global else None

    tools: list[tuple[str, str, str]] = []  # (key, name, description)

    if tool_type == "skills":
        items = list_global_skills() if is_global else list_project_skills(project)  # type: ignore[arg-type]
        tools = [(str(t.path), t.name, t.description) for t in items]

    elif tool_type == "agents":
        items = list_global_agents() if is_global else list_project_agents(project)  # type: ignore[arg-type]
        tools = [(str(t.path), t.name, t.description) for t in items]

    elif tool_type == "mcp":
        items = list_global_servers() if is_global else list_project_servers(project)  # type: ignore[arg-type]
        tools = [(t.name, t.name, f"{t.command} {' '.join(t.args)}".strip()) for t in items]

    elif tool_type == "memory" and not is_global:
        entries = list_entries(project)  # type: ignore[arg-type]
        tools = [(str(e.path), e.name, e.description) for e in entries]

    if not tools:
        return [("__empty__", f"  {DIM}(no {tool_type} installed){RESET}")]

    return [
        (
            key,
            f"  {BOLD_CYAN}{name:<30}{RESET}  {DIM}{desc}{RESET}",
        )
        for key, name, desc in tools
    ]


def tool_header(scope: str, tool_type: str) -> str:
    label = "GLOBAL" if scope == "GLOBAL" else Path(scope).name
    return (
        f"  {BOLD_CYAN}{label}{RESET} {DIM}/{RESET} {MAGENTA}{tool_type}{RESET}\n"
        f"  Enter: view  Ctrl-D: delete  Esc: back"
    )


def run_tools(scope: str, tool_type: str) -> tuple[str, str, str] | None:
    """Returns (scope, tool_type, key, pressed_key) tuple or None to go back."""
    items = tool_items(scope, tool_type)
    result = fzf(
        items,
        header=tool_header(scope, tool_type),
        prompt=f"  {tool_type}> ",
        expect=["ctrl-d"],
    )
    if not result.key or result.key == "__empty__":
        return None
    return scope, tool_type, result.key, result.pressed  # type: ignore[return-value]
