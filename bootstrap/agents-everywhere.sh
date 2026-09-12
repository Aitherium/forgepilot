#!/usr/bin/env bash
# Agents Everywhere: one terminal bootstrap for Linux, Termux, and macOS.
# Safe defaults: local services bind to loopback and optional bricks never receive secrets.
set -Eeuo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
AITHERIUM_HOME="${AITHERIUM_HOME:-${HOME}/.aitherium/agents-everywhere}"
MODEL="${AITHERIUM_MODEL:-bonsai-27b}"
RUN_PLAYBOOK="${AITHERZERO_PLAYBOOK:-1}"
RUN_LOCAL_MODEL="${AITHERIUM_RUN_LOCAL_MODEL:-1}"
HOST="${FORGEPILOT_HOST:-127.0.0.1}"
PORT="${FORGEPILOT_PORT:-8787}"
mkdir -p "$AITHERIUM_HOME/logs"

say() { printf '\n[agents-everywhere] %s\n' "$*"; }
warn() { printf '[agents-everywhere] warning: %s\n' "$*" >&2; }
has() { command -v "$1" >/dev/null 2>&1; }
try() {
  if ! "$@"; then
    warn "step failed (continuing): $*"
    return 1
  fi
}

say "detecting host"
if [[ -n "${TERMUX_VERSION:-}" || "${PREFIX:-}" == *com.termux* ]]; then
  PLATFORM="termux"
  say "Termux detected; installing user-space prerequisites"
  try pkg update -y || true
  if ! has python || ! has git || ! has node; then
    try pkg install -y python git nodejs-lts || try pkg install -y python git nodejs || true
  fi
elif has apt-get; then
  PLATFORM="linux-apt"
  if [[ "${AITHERIUM_INSTALL_OS_DEPS:-1}" == "1" ]]; then
    SUDO=""
    has sudo && SUDO="sudo"
    try $SUDO apt-get update || true
    try $SUDO apt-get install -y python3 python3-venv python3-pip git curl nodejs npm || true
  fi
elif has dnf; then
  PLATFORM="linux-dnf"
  if [[ "${AITHERIUM_INSTALL_OS_DEPS:-1}" == "1" ]]; then
    SUDO=""
    has sudo && SUDO="sudo"
    try $SUDO dnf install -y python3 python3-pip git curl nodejs npm || true
  fi
elif has brew; then
  PLATFORM="macos"
  try brew install python git node || true
else
  PLATFORM="generic-linux"
  say "using already-installed tools; install Python 3, Git, and Node.js if any are missing"
fi

PYTHON=""
if has python3; then PYTHON="$(command -v python3)"; elif has python; then PYTHON="$(command -v python)"; fi
if [[ -z "$PYTHON" ]]; then
  warn "Python 3 is required; install it and rerun this script"
  exit 2
fi
if ! has git; then
  warn "Git is required; install it and rerun this script"
  exit 2
fi

say "creating an isolated agent environment"
VENV="$AITHERIUM_HOME/.venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$PYTHON" -m venv "$VENV"; fi
PY="$VENV/bin/python"
"$PY" -m pip install --upgrade pip
if [[ -f "$ROOT/pyproject.toml" ]]; then "$PY" -m pip install -e "$ROOT"; fi

say "installing awdk and the MCP-capable base"
"$PY" -m pip install -U 'awdk[shell,platform,node]'

if [[ "${AITHERIUM_OPTIONAL_BRICKS:-1}" == "1" ]]; then
  for brick in awm awnode awrepl awgraph awgit awnboard; do
    try "$PY" -m pip install -U "$brick" || true
  done
  for repo in awiam awbac awdit awtunnel; do
    try "$PY" -m pip install -U "git+https://github.com/Aitherium/${repo}.git" || true
  done
fi

if has npm && [[ "${AITHERIUM_INSTALL_AWSH:-1}" == "1" ]]; then
  try npm install -g @aitherium/awsh || true
fi

if has git && has pwsh; then
  ZERO="$AITHERIUM_HOME/AitherZero"
  if [[ ! -d "$ZERO/.git" ]]; then
    try git clone --depth 1 https://github.com/Aitherium/AitherZero.git "$ZERO" || true
  fi
  if [[ -f "$ZERO/build.ps1" ]]; then
    say "building and checking AitherZero"
    try pwsh -NoProfile -Command "Set-Location -LiteralPath '$ZERO'; ./build.ps1; Import-Module ./AitherZero.psd1 -Force; Get-AitherStatus" || true
    if [[ "$RUN_PLAYBOOK" == "1" ]]; then
      say "running the AitherZero node-onboard playbook"
      try pwsh -NoProfile -Command "Set-Location -LiteralPath '$ZERO'; Import-Module ./AitherZero.psd1 -Force; Invoke-AitherPlaybook node-onboard" || true
    fi
  fi
else
  warn "PowerShell 7 is not available; skipping AitherZero orchestration (awdk path remains available)"
fi

if has adk && [[ "$RUN_LOCAL_MODEL" == "1" ]]; then
  say "requesting the local ${MODEL} path"
  try adk setup --tier bonsai --model "$MODEL" || true
  try adk bonsai-local --model "$MODEL" || true
  try adk start || true
else
  warn "adk is not on PATH or local model setup was disabled"
fi

if [[ -f "$ROOT/pyproject.toml" ]]; then
  say "starting the local MCP/WebMCP control surface on ${HOST}:${PORT}"
  nohup env FORGEPILOT_HOST="$HOST" FORGEPILOT_PORT="$PORT" "$PY" -m aitherium_pack serve \
    >"$AITHERIUM_HOME/logs/forgepilot.log" 2>&1 &
  echo $! >"$AITHERIUM_HOME/forgepilot.pid"
fi

cat >"$AITHERIUM_HOME/status.txt" <<EOF
platform=$PLATFORM
model=$MODEL
python=$PY
forgepilot=http://${HOST}:${PORT}
awdk=$(has adk && echo detected || echo missing)
awsh=$(has awsh && echo detected || echo missing)
awnode=$(has awnode && echo detected || echo missing)
EOF

say "bootstrap complete: detected is not the same as running or proven"
cat "$AITHERIUM_HOME/status.txt"
cat <<EOF

Next checks:
  "$PY" -m aitherium_pack mcp
  adk status
  awsh --version
  curl http://${HOST}:${PORT}/health

If the local model cannot fit this device, set AITHERIUM_RUN_LOCAL_MODEL=0 and use
an authenticated awnode/remote MCP endpoint. Never expose an unauthenticated MCP
port to the public internet; use awnboard/awiam/awbac/awdit and AitherConnect for
the approved phone/browser path.
EOF
