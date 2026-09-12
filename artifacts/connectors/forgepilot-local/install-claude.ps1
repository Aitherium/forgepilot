$ErrorActionPreference = 'Stop'
$root = "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon"
$py = "C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { throw 'Claude Code is not installed or is not on PATH.' }
claude mcp add forgepilot --scope project -- $py -m aitherium_pack mcp
Write-Host "ForgePilot MCP added to Claude Code for $root" -ForegroundColor Cyan
claude mcp get forgepilot
