# Executable desktop connectors

Generate the local connector artifact from the app or CLI:

```powershell
python -m aitherium_pack connector
```

It creates `artifacts/connectors/forgepilot-local/` with:

- `claude.mcp.json` — Claude Code project-scoped MCP config;
- `codex.mcp.json` — Codex MCP config;
- `install-claude.ps1` / `install-codex.ps1` — direct client registration;
- `bootstrap-full.ps1` — optional awdk/awsh/awiam/awbac/awdit/awtunnel install plus client registration;
- `install.sh` — macOS/Linux equivalent.

The generated scripts are intentionally explicit. `-InstallAwStack` installs packages; `-ConfigureClaude` and `-ConfigureCodex` modify client MCP configuration. The MCP server itself is stdio and local. For phones, use the HTTPS PWA connector and device flow instead.
