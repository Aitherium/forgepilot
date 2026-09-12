from __future__ import annotations

import os
import re
from typing import Iterable


MAX_HTTP_BODY = 1_048_576
MAX_TEXT = 16_000
MAX_DESCRIPTION = 8_000
MAX_EVIDENCE_ITEMS = 20
ALLOWED_SCOPES = frozenset({"local.inference", "mcp.tools", "workspace.read", "workspace.write", "memory", "repl", "lan.control"})
SAFE_PROFILE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
SAFE_MODEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,95}$")


def bounded_text(value: object, *, field: str, limit: int = MAX_TEXT) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if not value.strip():
        raise ValueError(f"{field} must not be empty")
    if len(value) > limit:
        raise ValueError(f"{field} exceeds the {limit}-character limit")
    return value


def validated_scopes(scopes: Iterable[object] | None, default: list[str]) -> list[str]:
    chosen = list(default if scopes is None else scopes)
    if not chosen or len(chosen) > len(ALLOWED_SCOPES):
        raise ValueError("invalid scope count")
    if any(not isinstance(scope, str) or scope not in ALLOWED_SCOPES for scope in chosen):
        raise ValueError("unknown or invalid capability scope")
    result = list(dict.fromkeys(chosen))
    if len(result) != len(chosen):
        raise ValueError("duplicate capability scope")
    return result


def valid_profile(profile: object) -> str:
    value = bounded_text(profile, field="profile", limit=64).lower()
    if not SAFE_PROFILE.fullmatch(value):
        raise ValueError("profile contains unsupported characters")
    return value


def valid_model(model: object) -> str:
    value = bounded_text(model, field="model", limit=96).strip()
    if not SAFE_MODEL.fullmatch(value):
        raise ValueError("model contains unsupported characters")
    return value


def bearer_token() -> str | None:
    token = os.getenv("FORGEPILOT_MCP_TOKEN", "").strip()
    return token or None


def allowed_origins(port: int) -> set[str]:
    configured = os.getenv("FORGEPILOT_ALLOWED_ORIGINS", "").strip()
    if configured:
        return {item.strip() for item in configured.split(",") if item.strip()}
    return {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}


def is_loopback(host: str) -> bool:
    return host in {"127.0.0.1", "localhost", "::1"}
