param(
  [string]$Profile = 'code',
  [int]$Timeout = 30
)
$ErrorActionPreference = 'Stop'

if (-not (Get-Command adk -ErrorAction SilentlyContinue)) {
  throw "adk is not installed. Run: irm https://aitherium.com/install.ps1 | iex"
}

if ($Profile -eq 'code') {
  & adk claude-model code
} elseif ($Profile -in @('plan','reason','local','fast')) {
  & adk claude-model $Profile
} else {
  & adk claude-model use $Profile
}
& adk claude-model status
& adk claude-model check --timeout $Timeout
