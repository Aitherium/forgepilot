param([switch]$InstallAwStack, [switch]$ConfigureClaude, [switch]$ConfigureCodex)
$ErrorActionPreference = 'Stop'
$root = "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon"
$py = "C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
Set-Location $root
if ($InstallAwStack) {
  & $py -m pip install awdk awm awnode awrepl awgraph awgit awnboard
  & $py -m pip install git+https://github.com/Aitherium/awiam.git git+https://github.com/Aitherium/awbac.git git+https://github.com/Aitherium/awdit.git git+https://github.com/Aitherium/awtunnel.git
  if (Get-Command npm -ErrorAction SilentlyContinue) { npm install -g @aitherium/awsh }
}
if ($ConfigureClaude) { & (Join-Path "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon\\artifacts\\connectors\\forgepilot-local" 'install-claude.ps1') }
if ($ConfigureCodex) { & (Join-Path "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon\\artifacts\\connectors\\forgepilot-local" 'install-codex.ps1') }
Write-Host 'Next: approve the ForgePilot project MCP server, then run the Aitherium device flow.' -ForegroundColor Cyan
Write-Host 'Local model: adk setup --tier bonsai --model bonsai-27b; adk bonsai-local --model bonsai-27b; adk start'
