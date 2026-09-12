$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (-not (Test-Path '.venv')) { python -m venv .venv }
$py = Join-Path $root '.venv\Scripts\python.exe'
& $py -m pip install --upgrade pip
& $py -m pip install -e . awdk awm awnode awrepl awgraph awgit awnboard
& $py -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
if (Get-Command npm -ErrorAction SilentlyContinue) { npm install -g @aitherium/awsh }
if (-not (Test-Path '.env')) { Copy-Item '.env.example' '.env' }
& $py -m aitherium_pack config
Write-Host 'Agents Everywhere bootstrap complete.' -ForegroundColor Cyan
Write-Host 'Security plane: awnboard -> awiam -> awbac -> awdit -> awtunnel' -ForegroundColor DarkCyan
Write-Host 'Next: adk setup --tier bonsai --model bonsai-27b'
Write-Host 'Then:  adk bonsai-local --model bonsai-27b; adk start'
Write-Host 'Auth:   awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control'
Write-Host 'Then:  python -m aitherium_pack serve'
