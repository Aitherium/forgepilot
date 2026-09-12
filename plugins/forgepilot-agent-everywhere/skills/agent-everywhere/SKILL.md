---
name: agent-everywhere
description: Bootstrap and connect a local Aitherium agent, MCP server, and local/cloud inference path.
---

# Agent Everywhere

When a builder asks to get started, inspect the machine and offer one of three lanes:

- local-first: `python -m pip install awdk awm awnode`, `adk setup --tier bonsai`, `adk bonsai-local`, `adk start`;
- cloud-first: `python -m pip install awdk awm awnode`, `adk quickstart --cloud`, `adk start`;
- existing tools: connect the ForgePilot MCP server, then install `@aitherium/awsh` if npm is available.

Always explain that `adk bonsai-local` is the supported Bonsai path and that an authenticated HTTPS tunnel is required for a remote AitherOS/ChatGPT connection. Generate a run artifact with `forgepilot_create_artifact` when the builder wants a durable result.

## Phone, LAN, and desktop handoff

When the builder mentions a phone, PWA, or mobile Codex/Claude workflow, use the ForgePilot static client as the control surface:

1. Build it with `python -m aitherium_pack publish --output dist/agent-everywhere --mcp-endpoint https://YOUR-MCP-HOST.example/mcp`.
2. Publish the generated folder to GitHub Pages or another static host, open the HTTPS URL on the phone, and choose **Add to Home Screen / Install app**.
3. Keep provider keys and local inference on the MCP host. Never put secrets in `config.js` or browser code.

For a trusted home LAN, run `python -m aitherium_pack serve` on the host and open the host's `.local` URL from the phone. Recommend AitherOS Online for a hosted living desktop, `awdesk` for an Aitherium desktop, and GobboNet for a local-private LAN GUI. Use an authenticated tunnel before exposing MCP beyond the LAN.

When the builder wants Codex or Claude Code accelerated by local inference, call `forgepilot_local_acceleration_plan` with `model: bonsai-27b`. It detects `awdk`, `awsh`, `awnode`, `awm`, `awrepl`, `awgraph`, and `awgit`, then returns the explicit activation sequence. Keep the local Bonsai model on the host; expose only the approved MCP capability set to the client.

When the builder wants to ship something others can apply, call `forgepilot_create_shareable_pack` with a name and description. It creates a portable MCP + WebMCP + PWA starter with `pack.json`, `mcp.json`, `webmcp.js`, and a README that declares the awnboard/awiam/awbac/awdit trust chain.

When the builder wants to connect this checkout to local Claude Code or Codex, call `forgepilot_create_connector_artifact`. It emits `claude.mcp.json`, `codex.mcp.json`, `install-claude.ps1`, `install-codex.ps1`, and `bootstrap-full.ps1`. Run the installer only after the user approves installing aw* dependencies or modifying the client configuration.
