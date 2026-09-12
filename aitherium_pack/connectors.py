from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


def create_connector_artifact(output_root: Path | None = None) -> dict[str, Any]:
    """Generate executable Claude Code + Codex connector files for this checkout."""
    target_root = output_root or ROOT / "artifacts" / "connectors"
    target = target_root / "forgepilot-local"
    target.mkdir(parents=True, exist_ok=True)
    py = str(Path(sys.executable).resolve())
    root = str(ROOT.resolve())
    claude = {"mcpServers": {"forgepilot": {"command": py, "args": ["-m", "aitherium_pack", "mcp"], "cwd": root, "env": {"PYTHONUNBUFFERED": "1"}}}}
    codex = {"mcp_servers": {"forgepilot": {"command": py, "args": ["-m", "aitherium_pack", "mcp"], "cwd": root, "env": {"PYTHONUNBUFFERED": "1"}}}}
    (target / "claude.mcp.json").write_text(json.dumps(claude, indent=2) + "\n", encoding="utf-8")
    (target / "codex.mcp.json").write_text(json.dumps(codex, indent=2) + "\n", encoding="utf-8")
    (target / "install-claude.ps1").write_text(f'''$ErrorActionPreference = 'Stop'
$root = {json.dumps(root)}
$py = {json.dumps(py)}
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {{ throw 'Claude Code is not installed or is not on PATH.' }}
claude mcp add forgepilot --scope project -- $py -m aitherium_pack mcp
Write-Host "ForgePilot MCP added to Claude Code for $root" -ForegroundColor Cyan
claude mcp get forgepilot
''', encoding="utf-8")
    (target / "install-codex.ps1").write_text(f'''$ErrorActionPreference = 'Stop'
$root = {json.dumps(root)}
$py = {json.dumps(py)}
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {{ throw 'Codex CLI is not installed or is not on PATH.' }}
codex mcp add forgepilot -- $py -m aitherium_pack mcp
Write-Host "ForgePilot MCP added to Codex" -ForegroundColor Cyan
codex mcp list
''', encoding="utf-8")
    (target / "bootstrap-full.ps1").write_text(f'''param([switch]$InstallAwStack, [switch]$ConfigureClaude, [switch]$ConfigureCodex)
$ErrorActionPreference = 'Stop'
$root = {json.dumps(root)}
$py = {json.dumps(py)}
Set-Location $root
if ($InstallAwStack) {{
  & $py -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  & $py -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  if (Get-Command npm -ErrorAction SilentlyContinue) {{ npm install -g @aitherium/awsh }}
}}
if ($ConfigureClaude) {{ & (Join-Path {json.dumps(str(target))} 'install-claude.ps1') }}
if ($ConfigureCodex) {{ & (Join-Path {json.dumps(str(target))} 'install-codex.ps1') }}
Write-Host 'Next: approve the ForgePilot project MCP server, then run the Aitherium device flow.' -ForegroundColor Cyan
Write-Host 'Local model: adk setup --tier bonsai --model bonsai-27b; adk bonsai-local --model bonsai-27b; adk start'
''', encoding="utf-8")
    (target / "install.sh").write_text(f'''#!/usr/bin/env bash
set -euo pipefail
ROOT={json.dumps(root)}
PYTHON={json.dumps(py)}
cd "$ROOT"
if [[ "${{INSTALL_AWSTACK:-0}}" == "1" ]]; then
  "$PYTHON" -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  "$PYTHON" -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  command -v npm >/dev/null 2>&1 && npm install -g @aitherium/awsh
fi
command -v claude >/dev/null 2>&1 && claude mcp add forgepilot --scope project -- "$PYTHON" -m aitherium_pack mcp || true
command -v codex >/dev/null 2>&1 && codex mcp add forgepilot -- "$PYTHON" -m aitherium_pack mcp || true
echo 'ForgePilot connector installed. Approve the project MCP server in Claude Code if prompted.'
''', encoding="utf-8")
    (target / "README.md").write_text(f'''# ForgePilot local connector

This artifact configures the same ForgePilot MCP server for Codex and Claude Code.

## One command on Windows

```powershell
.\\bootstrap-full.ps1 -InstallAwStack -ConfigureClaude -ConfigureCodex
```

Omit `-InstallAwStack` if you only want the MCP connector. Installing aw* packages may download dependencies; configuring the model remains explicit:

```powershell
adk setup --tier bonsai --model bonsai-27b
adk bonsai-local --model bonsai-27b
adk start
```

## Direct configs

- Claude Code: `claude.mcp.json` or `claude mcp add ...`
- Codex CLI: `codex.mcp.json` or `codex mcp add ...`

The generated connector uses stdio on the local machine. For phones or remote AitherOS, use the authenticated HTTPS MCP endpoint and device flow; do not expose local stdio or API keys.
''', encoding="utf-8")
    return {"path": str(target), "files": [p.name for p in target.iterdir()], "python": py, "project_root": root, "claude_config": claude, "codex_config": codex}
