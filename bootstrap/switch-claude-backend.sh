#!/usr/bin/env bash
set -Eeuo pipefail

PROFILE="${1:-code}"
TIMEOUT="${CLAUDE_CHECK_TIMEOUT:-30}"

if ! command -v adk >/dev/null 2>&1; then
  echo "adk is not installed. Run the Aitherium awsh installer first:" >&2
  echo "  curl -fsSL https://aitherium.com/install.sh | sh" >&2
  exit 2
fi

case "$PROFILE" in
  code|deepseek-flash)
    echo "Switching Claude Code to the DeepSeek Flash coding profile"
    if [[ "$PROFILE" == "code" ]]; then
      adk claude-model code
    else
      adk claude-model use deepseek-flash
    fi
    ;;
  plan|reason|local|fast)
    adk claude-model "$PROFILE"
    ;;
  *)
    adk claude-model use "$PROFILE"
    ;;
esac

adk claude-model status
adk claude-model check --timeout "$TIMEOUT"
