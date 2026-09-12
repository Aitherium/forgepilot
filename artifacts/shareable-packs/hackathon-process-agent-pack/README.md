# Hackathon Process Agent Pack

Turn this hackathon workflow into a shareable Codex + Claude + WebMCP pack with a local Bonsai path, awnboard authorization, and a phone-ready PWA.

This starter is shareable across Codex, Claude Code, AitherOS, and browser agents.

## Interfaces

- MCP: connect the local server or an authenticated HTTPS endpoint.
- WebMCP: load `webmcp.js` in a page that supports `document.modelContext`.
- PWA: publish the ForgePilot static bundle and point `config.js` at the MCP endpoint.

## Security

Requests pass through awnboard, awiam, awbac, and awdit. Keep API keys and local inference on the host.
