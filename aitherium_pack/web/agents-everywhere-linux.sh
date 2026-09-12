#!/bin/sh
# Agents Everywhere - Linux / Termux launcher.
#   sh agents-everywhere-linux.sh          (or make it executable and open it from your file manager)
# 1) AitherZero bootstrap: toolchain, adk, awsh  (dev-workstation; Termux runs the native lane)
# 2) connect: sign in (browser / device code), inference, wire your IDE to the MCP gateway
set -e
echo
echo "  Agents Everywhere - one command, this device becomes a connected agent node."
echo
curl -fsSL https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.sh | sh -s -- --playbook dev-workstation
if command -v pwsh >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.sh | sh -s -- --playbook connect
else
  # Termux / no-pwsh hosts: the connect steps by hand, same order as the playbook.
  adk login || adk login --github
  adk mcp setup --mode remote --ide claude-code || true
  adk mcp status || true
fi
echo
echo "  DONE. Type:  awsh"
echo
