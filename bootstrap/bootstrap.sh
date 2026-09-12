#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e . awdk awm awnode awrepl awgraph awgit awnboard
./.venv/bin/python -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
if command -v npm >/dev/null 2>&1; then npm install -g @aitherium/awsh; fi
test -f .env || cp .env.example .env
./.venv/bin/python -m aitherium_pack config
echo 'Agents Everywhere bootstrap complete.'
echo 'Security plane: awnboard -> awiam -> awbac -> awdit -> awtunnel'
echo 'Next: adk setup --tier bonsai --model bonsai-27b'
echo 'Then:  adk bonsai-local --model bonsai-27b; adk start'
echo 'Auth:   awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control'
echo 'Then:  python -m aitherium_pack serve'
