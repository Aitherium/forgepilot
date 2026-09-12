# AitherZero-first bootstrap

This is the Windows-friendly front door for the Agents Everywhere demo.

## Why AitherZero comes first

AitherZero is the orchestration layer. It can install and configure the Aitherium
products, run named playbooks, and report status. `awdk` then provides the agent
runtime, while `awsh` provides the shell/service surface. The demo keeps those
responsibilities separate so a generated artifact can be inspected before it is run.

## Playbook path

```powershell
git clone https://github.com/Aitherium/AitherZero.git
Set-Location AitherZero
./build.ps1
Import-Module ./AitherZero.psd1 -Force
Get-AitherStatus
Invoke-AitherPlaybook node-onboard
```

If the host is not ready for the playbook, install PowerShell 7 and the required
prerequisites first. Do not use a recipe that shells every step through `bash -lc` on
a blank Windows machine unless Git Bash or WSL is already present.

## Verify before connecting clients

```powershell
adk status
awsh --version
adk doctor
```

The expected state is observable, not inferred:

| State | Meaning |
| --- | --- |
| detected | the command/package exists |
| configured | the runtime has a saved configuration |
| authenticated | the user approved device/scopes |
| running | the local endpoint is live |
| proven | a real request returned from the intended local model |

The current hackathon machine has `awdk` and `awsh` detected, but the local inference
endpoints still need to be started and proven. That distinction is intentional.

## Continue into the demo

Use ForgePilot's **Activate Bonsai-27B stack** action to generate the next commands,
then **Configure Codex + Claude** to create client-specific MCP files. Keep the
requested scopes narrow (`local.inference`, `mcp.tools`, `workspace.read`, and only
the capabilities the tool needs). Put `awnboard → awiam → awbac → awdit` in front of
the shared surface before exposing it to a phone, LAN, or remote client.
