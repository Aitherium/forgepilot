# Agents Everywhere Demo Tool

Find the official MCP setup for this project and give me a safe Codex + Claude integration plan.

This starter is shareable across Codex, Claude Code, AitherOS, and browser agents.

## Interfaces

- MCP: connect the local server or an authenticated HTTPS endpoint.
- WebMCP: load `webmcp.js` in a page that supports `document.modelContext`.
- PWA: publish the ForgePilot static bundle and point `config.js` at the MCP endpoint.

## Security

Requests pass through awnboard, awiam, awbac, and awdit. Keep API keys and local inference on the host.
