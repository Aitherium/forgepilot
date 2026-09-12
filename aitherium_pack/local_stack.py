from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

from .security import valid_model


COMPONENTS = ["awdk", "awsh", "awnode", "awm", "awrepl", "awgraph", "awgit", "awiam", "awbac", "awnboard", "awdit", "awtunnel"]

COMMAND_ALIASES = {
    # awdk installs the `adk` CLI; awsh is commonly installed into the per-user
    # npm bin directory on Windows rather than the system PATH.
    "awdk": ("awdk", "adk"),
    "awsh": ("awsh",),
}


def _command_present(name: str) -> bool:
    candidates = COMMAND_ALIASES.get(name, (name,))
    if any(shutil.which(candidate) for candidate in candidates):
        return True
    if sys.platform == "win32":
        user_npm = Path.home() / "AppData" / "Roaming" / "npm"
        suffixes = (".cmd", ".ps1", ".exe", "")
        return any((user_npm / f"{candidate}{suffix}").exists() for candidate in candidates for suffix in suffixes)
    return False


def acceleration_plan(model: str = "bonsai-27b") -> dict[str, Any]:
    """Return a safe, read-only activation plan for the local Aitherium stack."""
    model = valid_model(model)
    detected = {name: _command_present(name) for name in COMPONENTS}
    python_packages = {}
    for package in COMPONENTS:
        try:
            __import__(package)
            python_packages[package] = True
        except ImportError:
            python_packages[package] = False
    return {
        "status": "ready_to_bootstrap",
        "model": model,
        "detected_commands": detected,
        "detected_python_packages": python_packages,
        "commands": [
            "# Universal terminal front door (review the script, then run on the host)",
            "curl -fsSL https://aitherium.com/install.sh | sh",
            "# Android Termux / Pixel Linux Terminal",
            "curl -fsSL https://aitherium.com/phone.sh | bash",
            "awsh --version",
            "git clone https://github.com/Aitherium/AitherZero.git",
            "Set-Location AitherZero; ./build.ps1",
            "Import-Module ./AitherZero.psd1 -Force",
            "Get-AitherStatus",
            "Invoke-AitherPlaybook node-onboard",
            "adk status",
            "awsh --version",
            f"{sys.executable} -m pip install awdk awm awrepl awgraph awgit awnboard",
            f"{sys.executable} -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git",
            f"adk setup --tier bonsai --model {model}",
            f"adk bonsai-local --model {model}",
            "adk start",
            "awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control",
            "awsh node register --name forgepilot-local --transport mcp --listen 127.0.0.1",
            "python -m aitherium_pack mcp",
        ],
        "codex_claude_role": "Use the local MCP surface for approved awm memory, awrepl interactive work, awgraph code context, and awgit project operations; keep Bonsai-27B inference on the host.",
        "security_plane": [
            "awnboard: front gate for the phone/PWA and remote client",
            "awiam: resolve the authenticated Aitherium caller and session",
            "awbac: fail-closed role/capability decisions",
            "awdit: append-only audit record for approvals and tool calls",
            "awtunnel: private reachability for a host with no public address",
        ],
        "capability_policy": {
            "local.inference": ["bonsai-27b", "awnode"],
            "mcp.tools": ["forgepilot", "awdk"],
            "workspace.read": ["awgraph", "awgit"],
            "workspace.write": ["awgit"],
            "memory": ["awm"],
            "repl": ["awrepl"],
            "lan.control": ["awnboard", "awtunnel"],
        },
        "safety": "This planner is read-only. Installation, device approval, LAN exposure, and workspace write access remain explicit user actions.",
    }
