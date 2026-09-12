from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .security import MAX_DESCRIPTION, bounded_text


ROOT = Path(__file__).resolve().parent.parent


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "agent-tool"


def create_shareable_pack(name: str, description: str, output_root: Path | None = None) -> dict[str, Any]:
    """Create a portable MCP + WebMCP + PWA-ready starter pack."""
    name = bounded_text(name, field="name", limit=160)
    description = bounded_text(description, field="description", limit=MAX_DESCRIPTION)
    pack_name = _slug(name)
    root = output_root or ROOT / "artifacts" / "shareable-packs"
    pack_dir = root / pack_name
    pack_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": pack_name,
        "display_name": name,
        "version": "0.1.0",
        "description": description,
        "interfaces": ["mcp", "webmcp", "pwa"],
        "auth": {"front_door": "awnboard", "identity": "awiam", "policy": "awbac", "audit": "awdit"},
        "capabilities": ["mcp.tools"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "entrypoints": {"local": "python -m aitherium_pack serve", "phone": "authenticated HTTPS MCP endpoint"},
    }
    (pack_dir / "pack.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (pack_dir / "README.md").write_text(
        f"# {name}\n\n{description}\n\n"
        "This starter is shareable across Codex, Claude Code, AitherOS, and browser agents.\n\n"
        "## Interfaces\n\n"
        "- MCP: connect the local server or an authenticated HTTPS endpoint.\n"
        "- WebMCP: load `webmcp.js` in a page that supports `document.modelContext`.\n"
        "- PWA: publish the ForgePilot static bundle and point `config.js` at the MCP endpoint.\n\n"
        "## Security\n\n"
        "Requests pass through awnboard, awiam, awbac, and awdit. Keep API keys and local inference on the host.\n",
        encoding="utf-8",
    )
    (pack_dir / "webmcp.js").write_text(
        "// Drop this file into a browser tool page. Keep execution behind your own MCP/policy boundary.\n"
        f"const tool = {{name:{json.dumps(pack_name)}, title:{json.dumps(name)}, description:{json.dumps(description)}, inputSchema:{{type:'object', properties:{{request:{{type:'string'}}}}}}, execute: async (input) => window.FORGEPILOT_EXECUTE(input)}};\n"
        "const modelContext = document.modelContext || navigator.modelContext;\n"
        "if (modelContext?.registerTool) await modelContext.registerTool(tool);\n",
        encoding="utf-8",
    )
    (pack_dir / "mcp.json").write_text(
        json.dumps({"mcpServers": {pack_name: {"command": "python", "args": ["-m", "aitherium_pack", "mcp"]}}}, indent=2) + "\n",
        encoding="utf-8",
    )
    return {"name": pack_name, "path": str(pack_dir), "manifest": manifest, "files": ["pack.json", "README.md", "webmcp.js", "mcp.json"]}
