$ErrorActionPreference = 'Stop'
python -m pip install -U awgym awrelay awsettings
if (Get-Command npm -ErrorAction SilentlyContinue) {
  npm install -g @aitherium/awsh
}
Write-Host 'Community bridge dependencies installed.' -ForegroundColor Cyan
Write-Host 'Next: awsh --version; adk status; https://arc.aitherium.com/'
Write-Host 'Do not place relay tokens or forum cookies in this repository.'
