# ForgePilot local connector

This artifact configures the same ForgePilot MCP server for Codex and Claude Code.

## One command on Windows

```powershell
.\bootstrap-full.ps1 -InstallAwStack -ConfigureClaude -ConfigureCodex
```

Omit `-InstallAwStack` if you only want the MCP connector. Installing aw* packages may download dependencies; configuring the model remains explicit:

```powershell
adk setup --tier bonsai --model bonsai-27b
adk bonsai-local --model bonsai-27b
adk start
```

## Direct configs

- Claude Code: `claude.mcp.json` or `claude mcp add ...`
- Codex CLI: `codex.mcp.json` or `codex mcp add ...`

The generated connector uses stdio on the local machine. For phones or remote AitherOS, use the authenticated HTTPS MCP endpoint and device flow; do not expose local stdio or API keys.
