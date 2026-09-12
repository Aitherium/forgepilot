#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e .
if [ "${SKIP_AWSDK:-0}" != "1" ]; then
  ./.venv/bin/python -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  ./.venv/bin/python -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  if [ "${SKIP_AWSH:-0}" != "1" ] && command -v npm >/dev/null 2>&1; then npm install -g @aitherium/awsh; fi
fi
test -f .env || cp .env.example .env
./.venv/bin/python -m aitherium_pack config
echo
echo 'ForgePilot is installed.'
echo 'Optional local activation: adk setup --tier bonsai --model bonsai-27b; adk bonsai-local --model bonsai-27b; adk start'
echo 'Optional device flow: awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control'
echo 'Add EXA_API_KEY and OPENROUTER_API_KEY to .env, then run:'
echo '  ./.venv/bin/python -m aitherium_pack serve'
