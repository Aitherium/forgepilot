$ErrorActionPreference = 'Stop'
Write-Host 'Review agents-everywhere-demo-tool before publishing.' -ForegroundColor Cyan
git add tools/agent/agents-everywhere-demo-tool
git diff --cached --check
Write-Host 'If correct: git commit -m "Add agents-everywhere-demo-tool agent tool"; git push'
