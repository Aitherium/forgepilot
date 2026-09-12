#!/bin/sh
# Agents Everywhere - macOS launcher. Double-click in Finder (Terminal opens by itself).
# 1) AitherZero bootstrap: PowerShell 7, toolchain, adk, awsh  (dev-workstation)
# 2) connect: sign in (browser), inference, wire Claude Code to the MCP gateway
# First run only: macOS may say the file is from an unidentified developer -
# right-click > Open once, or: xattr -d com.apple.quarantine "$0"
set -e
echo
echo "  Agents Everywhere - one click, this Mac becomes a connected agent node."
echo "  Step 1/2  tools    (Python, Git, Node, gh, adk, awsh)"
echo "  Step 2/2  connect  (sign in - a browser tab will open - inference, IDE wiring)"
echo
curl -fsSL https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.sh | sh -s -- --playbook dev-workstation
curl -fsSL https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.sh | sh -s -- --playbook connect
echo
echo "  DONE. Open a new terminal and type:  awsh"
echo "  (Claude Code / Cursor are already wired to the Aitherium MCP gateway.)"
echo
read -r -p "Press Enter to close. " _
