# Agents Everywhere Demo Tool

A shareable MCP and WebMCP tool for local agents

## Interfaces

- MCP: copy `mcp.json` into your client or use its CLI registration command.
- WebMCP: load `webmcp.js` only in a page with an authenticated executor.
- PWA: publish the static client over HTTPS; keep keys and inference on the host.

## Trust chain

`awnest` → `awnboard` → `awiam` → `awbac` → `awdit`

Requested capabilities: `mcp.tools, workspace.read`. Edit `policy.yaml` deliberately; default is deny.

## Prove it

1. Run the local MCP server.
2. Connect Codex or Claude Code.
3. Approve the requested capability as a human.
4. Invoke it and save the result.
