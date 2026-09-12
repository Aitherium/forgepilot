from __future__ import annotations

import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .security import validated_scopes


DEFAULT_SCOPES = ["local.inference", "mcp.tools", "workspace.read", "lan.control"]


def start_device_flow(scopes: list[str] | None = None, state_root: Path | None = None) -> dict[str, Any]:
    """Create a local, consent-scoped device-flow handoff.

    The local demo never receives or stores an Aitherium token. A real Aitherium
    deployment supplies AITHERIUM_DEVICE_URL and completes the exchange server-side.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=10)
    user_code = f"{secrets.token_hex(2).upper()}-{secrets.token_hex(2).upper()}"
    session_id = secrets.token_urlsafe(18)
    chosen_scopes = validated_scopes(scopes, DEFAULT_SCOPES)
    state_dir = state_root or Path.cwd() / ".forgepilot" / "device-sessions"
    state_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "session_id": session_id,
        "user_code_sha256": hashlib.sha256(user_code.encode()).hexdigest(),
        "scopes": chosen_scopes,
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "status": "awaiting_user_consent",
    }
    session_path = state_dir / f"{session_id}.json"
    session_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    try:
        session_path.chmod(0o600)
    except OSError:
        # Windows ACLs are managed by the user profile; do not fail the demo on chmod.
        pass
    device_url = os.getenv("AITHERIUM_DEVICE_URL", "https://aitherium.com/device")
    configured = bool(os.getenv("AITHERIUM_DEVICE_URL"))
    return {
        "status": "awaiting_user_consent",
        "mode": "aitherium-device-flow" if configured else "demo-device-flow",
        "session_id": session_id,
        "user_code": user_code,
        "verification_uri": device_url,
        "expires_in": 600,
        "scopes": chosen_scopes,
        "awsh_command": "awsh auth device --client-id forgepilot --scope " + " ".join(chosen_scopes),
        "note": "Demo mode creates a local handoff only; no token is issued until the Aitherium auth endpoint is configured and the user consents.",
    }
