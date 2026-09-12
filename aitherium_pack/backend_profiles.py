from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from .security import valid_profile


def _present(command: str) -> bool:
    return shutil.which(command) is not None


def switch_plan(profile: str = "deepseek-flash") -> dict[str, Any]:
    """Return the inspectable command plan for switching a coding-agent backend."""
    requested = valid_profile(profile.strip() or "deepseek-flash")
    adk = _present("adk")
    awsettings = _present("awsettings")
    aitheros_root = os.getenv("AITHEROS_ROOT")
    profile_tool = bool(aitheros_root and (Path(aitheros_root) / "dev" / "tools" / "claude_model_profile.py").exists())
    return {
        "status": "ready_to_switch" if adk else "missing_adk",
        "profile": requested,
        "alias": "adk claude-model code" if requested == "deepseek-flash" else f"adk claude-model use {requested}",
        "detected": {
            "adk": adk,
            "awsettings_command": awsettings,
            "claude_profile_tool": profile_tool,
        },
        "commands": [
            f"adk claude-model use {requested}",
            "adk claude-model status",
            "adk claude-model check --timeout 30",
        ],
        "fast_alias": "adk claude-model code",
        "other_profiles": [
            "adk claude-model plan",
            "adk claude-model reason",
            "adk claude-model local",
            "adk claude-model fast",
        ],
        "awsettings": {
            "detected": awsettings,
            "role": "Persist portable agent/provider settings and approvals; it is not a standalone executable on this host.",
            "safe_rule": "Keep provider keys in the local credential store; share profile names and scopes, never secret values.",
        },
        "verification": "A configured profile is not proven until adk claude-model check completes a real turn.",
        "note": "This planner does not change Claude Code, credentials, or provider selection. The user explicitly runs the command after reviewing it.",
    }
