#!/usr/bin/env bash
set -euo pipefail
ROOT="C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon"
PYTHON="C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
cd "$ROOT"
if [[ "${INSTALL_AWSTACK:-0}" == "1" ]]; then
  "$PYTHON" -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  "$PYTHON" -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  command -v npm >/dev/null 2>&1 && npm install -g @aitherium/awsh
fi
command -v claude >/dev/null 2>&1 && claude mcp add forgepilot --scope project -- "$PYTHON" -m aitherium_pack mcp || true
command -v codex >/dev/null 2>&1 && codex mcp add forgepilot -- "$PYTHON" -m aitherium_pack mcp || true
echo 'ForgePilot connector installed. Approve the project MCP server in Claude Code if prompted.'
