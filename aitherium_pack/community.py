from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .local_stack import _command_present
from .security import bounded_text


ROOT = Path(__file__).resolve().parent.parent
SURFACES = {
    "arc": "https://arc.aitherium.com/",
    "relay": "https://relay.aitherium.com/",
    "forums": "https://api.aitherium.com/",
    "spaces": "https://api.aitherium.com/",
    "awdesk": "https://github.com/Aitherium/awdesk",
    "awgym": "https://github.com/Aitherium/awgym",
    "awrelay": "https://github.com/Aitherium/awrelay",
    "awsettings": "https://github.com/Aitherium/awsettings",
}


def _importable(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False


def community_bridge_plan() -> dict[str, Any]:
    return {
        "status": "ready_to_connect",
        "surfaces": SURFACES,
        "detected": {
            "awgym": _importable("awgym"),
            "awrelay": _importable("awrelay"),
            "awsettings": _importable("awsettings"),
            "awsh": _command_present("awsh"),
            "awdk": _command_present("awdk") or _importable("awdk"),
        },
        "install_plan": [
            "python -m pip install -U awgym awrelay awsettings",
            "npm install -g @aitherium/awsh",
            "awsh --version",
            "adk status",
        ],
        "connection_plan": [
            "Open ARC and inspect the shared run/level record.",
            "Install awgym and run a local training/evaluation exercise.",
            "Install awrelay and configure a user-owned relay endpoint.",
            "Approve the device/session before joining Aitherium Relay or Spaces.",
            "Use AwDesk as the local desktop view of the same agent identity.",
            "Draft an introduction for forums/Spaces; send only after explicit approval.",
        ],
        "demo_sequence": [
            "ARC: show the living run graph and choose 'play it yourself'.",
            "AWGym: show the local gym/evaluation lane and its result artifact.",
            "AWRelay: show the transport/coordination boundary.",
            "Relay + Forums + Spaces: show where people and agents meet.",
            "AwDesk: show the desktop body receiving the same identity and events.",
        ],
        "security": {
            "default": "read-only plan; no forum post, relay message, invite, or account mutation",
            "identity": "awnest → awnboard → awiam → awbac → awdit",
            "rule": "never put relay tokens, forum cookies, or device credentials in a pack or PWA",
        },
    }


def create_community_bridge_pack(name: str = "Aitherium Community Bridge", output_root: Path | None = None) -> dict[str, Any]:
    name = bounded_text(name, field="name", limit=160)
    slug = "aitherium-community-bridge"
    root = output_root or ROOT / "artifacts" / "community-bridge"
    pack_dir = root / slug
    pack_dir.mkdir(parents=True, exist_ok=True)
    plan = community_bridge_plan()
    manifest = {
        "name": slug,
        "display_name": name,
        "version": "0.1.0",
        "interfaces": ["mcp", "awsh", "arc", "awgym", "awrelay", "awdesk"],
        "surfaces": plan["surfaces"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "secrets": "none",
    }
    (pack_dir / "pack.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (pack_dir / "README.md").write_text(
        f"# {name}\n\n"
        "Connect an Aitherium agent from ARC/AWGym through awrelay to Relay, Forums, Spaces, and AwDesk.\n\n"
        "## Install\n\n"
        "```bash\npython -m pip install -U awgym awrelay awsettings\nnpm install -g @aitherium/awsh\nawsh --version\n```\n\n"
        "## Safety\n\n"
        "This pack contains no tokens and does not post, invite, or send messages. Review the target surface, approve identity/scopes, and perform any outbound action explicitly.\n\n"
        "## Surfaces\n\n"
        + "\n".join(f"- [{key}]({url})" for key, url in SURFACES.items())
        + "\n",
        encoding="utf-8",
    )
    (pack_dir / "relay-config.example.json").write_text(
        json.dumps({"relay_url": SURFACES["relay"], "agent_id": "replace-me", "scopes": ["mcp.tools", "workspace.read"], "token": "<never-commit>"}, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack_dir / "demo.md").write_text(
        "# 90-second community loop\n\n"
        "1. Open ARC and show the run graph.\n"
        "2. Run one AWGym evaluation and save the result.\n"
        "3. Show awrelay as the transport boundary.\n"
        "4. Open Relay/Forums/Spaces and draft, but do not auto-send, an introduction.\n"
        "5. Open AwDesk and show the same identity as a desktop surface.\n\n"
        "The ForgePilot MCP tool exposes this as a read-only plan; the human remains the sender.\n",
        encoding="utf-8",
    )
    return {"path": str(pack_dir), "manifest": manifest, "files": [p.name for p in pack_dir.iterdir()]}
