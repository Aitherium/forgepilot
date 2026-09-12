$ErrorActionPreference = 'Stop'
$root = "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon"
$py = "C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'Codex CLI is not installed or is not on PATH.' }
codex mcp add forgepilot -- $py -m aitherium_pack mcp
Write-Host "ForgePilot MCP added to Codex" -ForegroundColor Cyan
codex mcp list
