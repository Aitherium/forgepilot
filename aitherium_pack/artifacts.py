from __future__ import annotations

import hashlib
import json
import platform
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .providers import exa_search, openrouter_chat
from .security import bounded_text


ROOT = Path(__file__).resolve().parent.parent


def _aw_stack_status() -> dict[str, bool]:
    packages = ["awdk", "awm", "awresearch", "awfind", "awbrowse", "awrun", "awrelay", "awgraph", "awgit", "awseal", "awshare"]
    status: dict[str, bool] = {}
    for package in packages:
        try:
            __import__(package)
            status[package] = True
        except ImportError:
            status[package] = False
    return status


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def create_run(request: str, output_root: Path | None = None) -> dict[str, Any]:
    request = bounded_text(request, field="request")
    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S") + f"-{secrets.token_hex(3)}Z"
    target_root = output_root or ROOT / "artifacts" / "runs"
    run_dir = target_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    evidence = exa_search(request)
    answer = openrouter_chat(request, evidence.get("results", []))
    stack = _aw_stack_status()
    report = f"""# ForgePilot run {run_id}

## Request

{request}

## Result

{answer.get('content', '')}

## Evidence

""" + "\n".join(
        f"- [{item.get('title', 'Source')}]({item.get('url', '')})\n  - " + "\n  - ".join(item.get("highlights", []))
        for item in evidence.get("results", [])
    ) + f"""

## Runtime

- Research mode: `{evidence.get('mode', 'unknown')}`
- Model mode: `{answer.get('mode', 'unknown')}`
- aw* packages detected: `{sum(stack.values())}/{len(stack)}`
- Host: `{platform.system()} {platform.release()}`

## Next action

Review the evidence, then attach this report and the generated MCP config to the target desktop agent. This run is read-only and does not mutate the repository.
"""

    files: dict[str, bytes] = {
        "request.json": _json_bytes({"request": request, "created_at": now.isoformat()}),
        "research.json": _json_bytes(evidence),
        "response.json": _json_bytes(answer),
        "stack.json": _json_bytes(stack),
        "report.md": report.encode("utf-8"),
    }
    manifest: dict[str, Any] = {"run_id": run_id, "created_at": now.isoformat(), "files": {}}
    for name, content in files.items():
        path = run_dir / name
        path.write_bytes(content)
        manifest["files"][name] = {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
    manifest_bytes = _json_bytes(manifest)
    (run_dir / "manifest.json").write_bytes(manifest_bytes)
    return {"run_id": run_id, "path": str(run_dir), "report": str(run_dir / "report.md"), "manifest": manifest}
