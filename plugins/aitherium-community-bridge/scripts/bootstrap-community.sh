#!/usr/bin/env bash
set -Eeuo pipefail

python3 -m pip install -U awgym awrelay awsettings
if command -v npm >/dev/null 2>&1; then
  npm install -g @aitherium/awsh
fi

echo 'Community bridge dependencies installed.'
echo 'Next: awsh --version && adk status'
echo 'Then open ARC: https://arc.aitherium.com/'
echo 'Do not place relay tokens or forum cookies in this repository.'
