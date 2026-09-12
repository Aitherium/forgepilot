# Shareable agentic + WebMCP packs

ForgePilot is a pack factory. A builder can use the browser button, Codex MCP, Claude Code, or the CLI:

```powershell
python -m aitherium_pack pack "My Agent Tool" "What this tool does for another builder."
```

The generated folder contains:

- `pack.json` — portable identity, interfaces, entrypoints, and trust chain;
- `mcp.json` — desktop MCP connection starter;
- `webmcp.js` — browser-native tool registration starter;
- `README.md` — phone/PWA and security handoff.

The pack is intentionally a starter: the author supplies the real executor behind `window.FORGEPILOT_EXECUTE` and connects it to their MCP server. The shared contract remains the same across Codex, Claude Code, AitherOS, a phone PWA, and any WebMCP-capable browser.

Security is part of the pack metadata: `awnboard` is the front door, `awiam` identifies the caller, `awbac` evaluates capabilities, and `awdit` records decisions. A public PWA must use an authenticated HTTPS MCP endpoint; it must never contain local provider keys.
