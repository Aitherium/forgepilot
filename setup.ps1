$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
if (-not (Test-Path '.venv')) { python -m venv .venv }
$py = Join-Path $root '.venv\Scripts\python.exe'
& $py -m pip install --upgrade pip
& $py -m pip install -e .
if ($env:SKIP_AWSDK -ne '1') {
  & $py -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  & $py -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  if ($env:SKIP_AWSH -ne '1' -and (Get-Command npm -ErrorAction SilentlyContinue)) { npm install -g @aitherium/awsh }
}
if (-not (Test-Path '.env')) { Copy-Item '.env.example' '.env' }
& $py -m aitherium_pack config
Write-Host ''
Write-Host 'ForgePilot is installed.' -ForegroundColor Cyan
Write-Host 'Optional local activation: adk setup --tier bonsai --model bonsai-27b; adk bonsai-local --model bonsai-27b; adk start'
Write-Host 'Optional device flow: awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control'
Write-Host 'Add EXA_API_KEY and OPENROUTER_API_KEY to .env, then run:'
Write-Host '  .\.venv\Scripts\python.exe -m aitherium_pack serve'
