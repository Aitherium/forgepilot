#!/usr/bin/env bash
set -euo pipefail
echo 'Review agents-everywhere-demo-tool before publishing.'
git add tools/agent/agents-everywhere-demo-tool
git diff --cached --check
echo 'If correct: git commit -m "Add agents-everywhere-demo-tool agent tool"; git push'
