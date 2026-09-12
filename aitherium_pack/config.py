from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _server_command() -> dict[str, object]:
    return {
        "command": sys.executable,
        "args": ["-m", "aitherium_pack", "mcp"],
        "cwd": str(ROOT),
        "env": {"PYTHONUNBUFFERED": "1"},
    }


def configs() -> dict[str, dict[str, object]]:
    server = _server_command()
    return {
        "claude.mcp.json": {"mcpServers": {"forgepilot": server}},
        "codex.mcp.json": {"mcp_servers": {"forgepilot": server}},
        "remote-mcp.json": {
            "name": "forgepilot",
            "url": f"http://{os.getenv('FORGEPILOT_HOST', '127.0.0.1')}:{os.getenv('FORGEPILOT_PORT', '8787')}/mcp",
            "transport": "streamable-http",
        },
        "openrouter.tool.json": {
            "provider": "openrouter",
            "base_url": "https://openrouter.ai/api/v1",
            "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            "tools_endpoint": "/mcp",
        },
        "exa.tool.json": {
            "provider": "exa",
            "base_url": "https://api.exa.ai",
            "search_type": "auto",
            "contents": {"highlights": True},
        },
    }


def write_configs(output_dir: Path | None = None) -> list[Path]:
    target = output_dir or ROOT / "integrations" / "generated"
    target.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for name, payload in configs().items():
        path = target / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        paths.append(path)
    return paths
